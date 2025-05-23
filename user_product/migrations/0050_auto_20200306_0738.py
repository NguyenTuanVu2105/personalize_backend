# Generated by Django 2.2 on 2019-11-05 15:29
from django.db import migrations

from user_product.models import Artwork, ArtworkFusion


def copy_artwork_to_artwork_fusion(apps, schema_editor):
    for artwork in Artwork.objects.all():
        ArtworkFusion.objects.create(id=artwork.id, owner=artwork.owner, name=artwork.name, original_image_path=artwork.original_image_path)


class Migration(migrations.Migration):
    dependencies = [
        ('user_product', '0049_auto_20200306_0737'),
    ]

    operations = [
        migrations.RunPython(copy_artwork_to_artwork_fusion),
    ]
