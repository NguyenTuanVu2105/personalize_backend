from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AbstractProductConfig(AppConfig):
    name = 'abstract_product'
    verbose_name = _("Abstract Product")
    verbose_name_plural = _("Abstract Products")
    def ready(self):
        import abstract_product.signals
