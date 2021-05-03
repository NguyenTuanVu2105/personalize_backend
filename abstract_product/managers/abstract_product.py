from django.db.models import Manager, QuerySet

from abstract_product.constants import AbstractType


class BaseAbstractProductManager(Manager):
    pass


class AbstractProductQueryset(QuerySet):
    def branding_card_only(self):
        return self.filter(type=AbstractType.BRANDING_CARD)

    def product_only(self):
        return self.filter(type__in=[AbstractType.AOP_PRODUCT, AbstractType.FLAT_PRODUCT])

    def aop_product_only(self):
        return self.filter(type=AbstractType.AOP_PRODUCT)

    def flat_product_only(self):
        return self.filter(type=AbstractType.FLAT_PRODUCT)

    def active_visible_filter(self):
        return self.filter(is_active=True, is_catalog_visible=True)


AbstractProductManager = BaseAbstractProductManager.from_queryset(AbstractProductQueryset)
