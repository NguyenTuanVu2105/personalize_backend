from django.contrib.auth.models import UserManager as BaseUserManager


class UserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().select_related("settings")

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        super().create_superuser(username="_", email=email, password=password, **extra_fields)
