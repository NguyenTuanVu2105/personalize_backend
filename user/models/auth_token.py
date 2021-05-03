from django.db import models

from user.contants.login_type import LOGIN_TYPE_CHOICES, LoginType


class AuthToken(models.Model):
    token = models.CharField(max_length=256)
    user_id = models.BigIntegerField()
    is_revoked = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=2, choices=LOGIN_TYPE_CHOICES, default=LoginType.WEB)
    last_used_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'auth_token'
        ordering = ['id']
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['user_id']),
            models.Index(fields=['is_revoked']),
        ]
