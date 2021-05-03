from django.db.models import QuerySet, Manager


class BaseGeneralPaymentMethodManager(Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("user_setting").prefetch_related("content_object")


class GeneralPaymentMethodQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def by_user(self, user_id):
        return self.filter(user_setting__user=user_id)


GeneralPaymentMethodManager = BaseGeneralPaymentMethodManager.from_queryset(GeneralPaymentMethodQuerySet)
