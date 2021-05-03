import logging

from django.db import models
from django.db.models import QuerySet, Q

logger = logging.getLogger(__name__)


class BaseUserProductArtworkFusionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('user_product', 'product_side', 'artwork_fusion')


class UserProductArtworkFusionQueryset(QuerySet):
    def is_visible(self):
        return self.filter(
            Q(user_product__abstract_product__meta__fusion_meta__fusion_combination=True,
              send_to_fulfill=False) | Q(
                user_product__abstract_product__meta__fusion_meta__fusion_combination=False,
                send_to_fulfill=True))

    def send_to_fulfill_filter(self):
        return self.filter(send_to_fulfill=True)

    def send_to_fulfill_exclude(self):
        return self.filter(send_to_fulfill=False)


UserProductArtworkFusionManager = BaseUserProductArtworkFusionManager.from_queryset(UserProductArtworkFusionQueryset)
