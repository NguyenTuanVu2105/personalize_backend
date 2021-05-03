from django.db import migrations

from HUB.models.random_id_model import RandomIDModel
from user_product.models import TextPersonalization, UserFontFamily


def random_id_model(apps, schema_editor):
    RandomIDModel.init_random_seq(TextPersonalization)
    RandomIDModel.init_random_seq(UserFontFamily)


class Migration(migrations.Migration):
    dependencies = [
        ('user_product', '0126_textpersonalization_userfontfamily'),
    ]

    operations = [
        migrations.RunPython(random_id_model),
    ]
