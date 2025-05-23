# Generated by Django 2.2.2 on 2020-07-28 07:01

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0023_create_text_search_trigger'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supportticket',
            name='read_conversation',
        ),
        migrations.RemoveField(
            model_name='supportticket',
            name='tags',
        ),
        migrations.AddField(
            model_name='supportticket',
            name='attachments',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True), blank=True, default=[], null=True, size=None),
        ),
    ]
