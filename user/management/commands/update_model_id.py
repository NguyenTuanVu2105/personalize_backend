import logging

from django.apps import apps
from django.core.management.base import BaseCommand

from billing.sub_apps.braintree_payment.services import create_braintree_customer
from helper.model_helpers import unique_id_generator

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Update old model id (length < 5) to new random id format'

    def add_arguments(self, parser):
        parser.add_argument('--model', type=str, help='Enter <app_name>.<model_name>')

    def handle(self, *args, **kwargs):
        model_path = kwargs.get("model")
        if model_path:
            app_name, model_name = model_path.split(".")
            model = apps.get_model(app_name, model_name)
            logger.info("Merge new random id for model", model)
            old_id_objects = model.objects.filter(id__lte=10000)
            for obj in old_id_objects:
                new_id = unique_id_generator(obj)
                logger.info("Updating {} to new id {}".format(obj, new_id))
                model.objects.filter(id=obj.id).update(id=new_id)
                obj.save()
                if model_name == "User":
                    create_braintree_customer(obj)
            logger.info("Done updating random id for model", model)
