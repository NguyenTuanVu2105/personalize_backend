from django.db.models import Manager, QuerySet


class BaseUserSettingsManager(Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("user")


class UserSettingsQueryset(QuerySet):
    pass


UserSettingsManager = BaseUserSettingsManager.from_queryset(UserSettingsQueryset)
