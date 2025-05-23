# Generated by Django 2.2.2 on 2020-10-17 09:04

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import shop.models.shop_token


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_auto_20201016_0645'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopToken',
            fields=[
                ('id', models.BigAutoField(db_index=True, primary_key=True, serialize=False, unique=True)),
                ('shop_url', models.CharField(default='', max_length=100)),
                ('code', models.TextField(unique=True)),
                ('shopify_response', django.contrib.postgres.fields.jsonb.JSONField(default=shop.models.shop_token.default_shopify_response)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'shop_token',
                'ordering': ['-create_time'],
            },
        ),
    ]
