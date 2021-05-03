from django.db import migrations


def migrate_artwork_default_sku(apps, schema_editor):
    ArtworkDefault = apps.get_model("user_product", "ArtworkDefault")
    default_artworks = ArtworkDefault.objects.all()
    for default_artwork in default_artworks:
        if not default_artwork.product_sku:
            sku = default_artwork.product_side.abstract_product.sku
            if sku:
                default_artwork.product_sku = sku
                default_artwork.save()


class Migration(migrations.Migration):
    dependencies = [
        ('user_product', '0100_artworkdefault_product_sku'),
    ]

    operations = [
        migrations.RunPython(migrate_artwork_default_sku),
    ]
