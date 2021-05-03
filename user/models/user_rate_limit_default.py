from django.db import models
from django.utils.translation import gettext as _

from ..contants.rate_limit_views import RATE_LIMIT_VIEW_CHOICES, RateLimitView


class UserRateLimitDefault(models.Model):
    view = models.CharField(primary_key=True, max_length=2, choices=RATE_LIMIT_VIEW_CHOICES, default=RateLimitView.CREATE_USER_PRODUCT, blank=True)
    rate_limit = models.IntegerField(default=0)

    class Meta:
        db_table = 'user_rate_limit_default'
        ordering = ['view']
        verbose_name = _("User Rate Limit Default")
        verbose_name_plural = _("User Rate Limit Defaults")
