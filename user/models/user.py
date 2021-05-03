from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from user.managers import UserManager
from .user_settings import UserSettings
from ..contants import AccountType, ACCOUNT_TYPE_CHOICES

GENDER_CHOICES = (
    (_('Male'), _('Male')),
    (_('Female'), _('Female')),
    (_('Other'), _('Other'))
)


class User(AbstractUser, RandomIDModel):
    avatar = models.TextField(null=True, blank=True, verbose_name=_('Avatar'))
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Phone Number'))
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, null=True, blank=True, verbose_name=_('Gender'))
    tax_code = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Tax Code'))
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, related_name='users_set')
    birthday = models.DateField(null=True, blank=True, verbose_name=_('Birthday'))
    address = models.CharField(max_length=120, null=True, blank=True, verbose_name=_('Address'))
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=120, verbose_name=_('Name'))
    # products = models.ManyToManyField(AbstractProduct, through='user.UserProduct', related_name='products_list')
    is_email_confirmed = models.BooleanField(default=True)
    is_valid_payment = models.BooleanField(default=False)
    is_test_user = models.BooleanField(default=False)
    is_lock = models.BooleanField(default=False)
    account_type = models.CharField(max_length=2, default=AccountType.EMAIL, choices=ACCOUNT_TYPE_CHOICES)
    token_confirmation = models.CharField(max_length=50, null=True)
    token_confirmation_expire_time = models.DateTimeField(null=True)

    token_forgot_password = models.CharField(max_length=50, null=True)
    token_forgot_password_expire_time = models.DateTimeField(null=True)

    last_change_password = models.DateTimeField(null=True)
    last_send_failed_payment_noti = models.DateTimeField(null=True)
    message_id = models.CharField(max_length=50, null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    throttling_rate_factor = models.SmallIntegerField(default=10)
    client_ip = models.GenericIPAddressField(null=True, blank=True)
    country_code = models.CharField(max_length=2, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    tsv_metadata_search = SearchVectorField(null=True)

    class Meta:
        db_table = 'user'
        ordering = ['id']
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        indexes = [GinIndex(fields=["tsv_metadata_search"])]

    def is_admin(self):
        return True if self.is_superuser else False

    def is_seller(self):
        return True if not self.is_superuser else False

    # def is_seller(self):
    #     return True if 'seller' in str(self.group) else False

    def parse_basic_info(self):
        info = {
            "id": self.id,
            "username": self.username
        }
        return info

    def create_user_settings(self):
        return UserSettings.objects.create(user=self)

    @property
    def existed_time(self):
        return datetime.now(self.create_time.tzinfo) - self.create_time
