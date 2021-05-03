from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from . import User
from ..contants.rate_limit_views import RATE_LIMIT_VIEW_CHOICES, RateLimitView


class UserLimit(RandomIDModel):
    view = models.CharField(max_length=2, choices=RATE_LIMIT_VIEW_CHOICES, default=RateLimitView.CREATE_USER_PRODUCT, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='rate_limits')
    rate_limit = models.IntegerField(default=0)

    class Meta:
        db_table = 'user_rate_limit'
        unique_together = ('view' , 'user')
        ordering = ['id']
        verbose_name = _("User Rate Limit")
        verbose_name_plural = _("User Rate Limits")
        indexes = [
            models.Index(fields=['user', 'view', ]),
        ]
