from datetime import timedelta

from django.contrib.postgres.fields import JSONField
from django.db import models, transaction
from django.db.models import PositiveSmallIntegerField
from django.utils import timezone
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from billing.sub_apps.combine_payment.constants.charge_constants import SEND_NOTIFICATION_AFTER_X_FAILED_CHARGE, \
    STOP_AFTER_X_FAILED_CHARGES
from helper.datetime_helpers import get_current_datetime
from user.contants import TIMEZONE_CHOICES
from user.contants.time_delays import EDIT_ORDER_ITEMS_DELAY
from user.contants.tracking_generation_time import TrackingGenerationTime
from user.managers import UserSettingsManager


class UserSettings(RandomIDModel):
    user = models.OneToOneField(to='user.User', related_name="settings", on_delete=models.CASCADE)

    failed_charge_count = PositiveSmallIntegerField(default=0)
    next_charge_time = models.DateTimeField(default=timezone.now)
    last_create_support_ticket_time = models.DateTimeField(default=timezone.now)
    timezone = models.CharField(max_length=50, default="Etc/UTC", choices=TIMEZONE_CHOICES)
    edit_order_items_delay = models.DurationField(default=timedelta(seconds=EDIT_ORDER_ITEMS_DELAY))
    request_order_processing_manually = models.BooleanField(default=False)
    tracking_generation_time = models.IntegerField(default=TrackingGenerationTime.AT_PACKAGING_STAGE)
    default_branding_card = models.ForeignKey('user_product.UserVariant', null=True, on_delete=models.SET_NULL)

    objects = UserSettingsManager()

    class Meta:
        db_table = 'user_settings'
        ordering = ['id']
        verbose_name = _('User Settings')
        verbose_name_plural = _('User Settings')

    def __str__(self):
        return "Settings of {}".format(self.user)

    @property
    def should_halt_to_charge_invoices(self):
        return self.failed_charge_count >= STOP_AFTER_X_FAILED_CHARGES

    @property
    def is_invoices_charge_unlockable(self):
        return self.user.invoices.failed().count() > 0

    @property
    def should_send_failed_notification(self):
        return self.failed_charge_count == SEND_NOTIFICATION_AFTER_X_FAILED_CHARGE

    @transaction.atomic
    def unlock_invoices_charge(self):
        self.failed_charge_count = 0
        self.next_charge_time = get_current_datetime()
        self.save()

        from notification.services.instant_prompt import remove_instant_payment_prompt
        remove_instant_payment_prompt(self.user_id)

    @property
    def just_had_some_failed_charges(self):
        current_time = get_current_datetime()
        return current_time < self.next_charge_time
