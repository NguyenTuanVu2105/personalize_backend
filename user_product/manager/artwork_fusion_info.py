import logging

from django.db import models
from django.db.models import QuerySet, Q

logger = logging.getLogger(__name__)


class BaseArtworkFusionInfoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('layer')


class ArtworkFusionInfoQueryset(QuerySet):
    def is_visible(self):
        return self.filter(is_hidden=False)


ArtworkFusionInfoManager = BaseArtworkFusionInfoManager.from_queryset(ArtworkFusionInfoQueryset)
