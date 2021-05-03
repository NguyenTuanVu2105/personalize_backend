import logging

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

logger = logging.getLogger(__name__)


class ActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


class ForgotPasswordTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # now = datetime.utcnow().strftime("%Y%m%d%HH%MM%SS")
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = ActivationTokenGenerator()
forgot_password_token = ForgotPasswordTokenGenerator()
