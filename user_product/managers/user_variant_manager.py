from django.db.models import Manager, QuerySet


class BaseUserVariantManager(Manager):
    pass


class UserVariantQueryset(QuerySet):
    def prefetch_related_objects(self):
        return self.select_related("abstract_variant", "user_product").prefetch_related(
            "abstract_variant__attributes_value", "abstract_variant__attributes_value__attribute", "mockup_per_side")


UserVariantManager = BaseUserVariantManager.from_queryset(UserVariantQueryset)
