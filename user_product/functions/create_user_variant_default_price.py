import logging

from celery.decorators import task
from django.contrib.auth import get_user_model
from django.db import transaction

from HUB.constants.celery_task import CeleryTask
from abstract_product.models import AbstractProductVariant
from user_product.models import UserAbstractVariantDefaultPrice

User = get_user_model()

logger = logging.getLogger(__name__)


@task(name=CeleryTask.TASK_CREATE_USER_VARIANT_DEFAULT_PRICE)
def create_user_variant_default_price(variants, seller_id):
    with transaction.atomic():
        seller = User.objects.get(pk=seller_id)
        for variant in variants:
            abstract_variant_id = variant['abstract_variant']
            abstract_variant = AbstractProductVariant.objects.get(id=abstract_variant_id)
            for k in variant['price']:
                value = variant['price'][k]['value']
                UserAbstractVariantDefaultPrice.objects.update_or_create(
                    abstract_variant=abstract_variant, currency=k, user=seller, defaults={'price': value})
