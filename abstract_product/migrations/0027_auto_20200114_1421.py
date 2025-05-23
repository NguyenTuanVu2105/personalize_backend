# Generated by Django 2.2.2 on 2020-01-14 14:20
import logging

from django.db import migrations, connection

from HUB.models.random_id_model import RandomIDModel

logger = logging.getLogger(__name__)


def init_random_model(apps, schema_editor):
    print(apps.get_models())
    with connection.cursor() as cursor:
        cursor.execute("CREATE OR REPLACE FUNCTION nextval_rand(regclass) RETURNS bigint AS $func$ BEGIN EXECUTE format('ALTER SEQUENCE %s INCREMENT %s', $1, (random() * 1000)::bigint + 1); RETURN nextval($1)::bigint; END $func$ LANGUAGE plpgsql SECURITY DEFINER;")
    for model in apps.get_models():
        app_model = apps.get_model(model._meta.app_label, model._meta.object_name)
        print(app_model)
        print(model._meta.app_label)
        print(model._meta.object_name)
        try:
            print(model._meta.get_field('id'))
            RandomIDModel.init_random_seq(app_model)
        except Exception as e:
            logger.exception(e)
            # model.__class__.init_random_seq()


class Migration(migrations.Migration):
    dependencies = [
        ('abstract_product', '0026_auto_20200113_1332'),
    ]

    operations = [
        migrations.RunPython(init_random_model),
    ]
