# Generated by Django 2.2.2 on 2020-07-17 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0011_update_coversation_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportticketconversation',
            name='conversation_id',
            field=models.BigIntegerField(db_index=True, unique=True),
        ),
    ]
