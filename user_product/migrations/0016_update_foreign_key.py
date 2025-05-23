# Generated by Django 2.2.2 on 2019-10-26 16:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('user_product', '0015_userabstractvariantdefaultprice'),
    ]

    operations = [
        migrations.RunSQL('alter table user_product_artwork alter column artwork_id type bigint using artwork_id::bigint;'),
        migrations.RunSQL('alter table user_product_artwork alter column product_side_id type bigint using product_side_id::bigint;'),
        migrations.RunSQL('alter table user_product_artwork alter column user_product_id type bigint using user_product_id::bigint'),
        migrations.RunSQL('alter table user_variant_price alter column user_variant_id type bigint using user_variant_id::bigint'),
        migrations.RunSQL('alter table user_variant alter column user_product_id type bigint using user_product_id::bigint'),
        migrations.RunSQL('alter table user_variant_side_mockup alter column product_side_id type bigint using product_side_id::bigint'),
        migrations.RunSQL('alter table user_variant_side_mockup alter column user_variant_id type bigint using user_variant_id::bigint')
    ]
