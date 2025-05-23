# Generated by Django 2.2.2 on 2019-10-24 14:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('abstract_product', '0007_auto_20191017_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractproduct',
            name='id',
            field=models.BigAutoField(db_index=True, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='abstractproductcategory',
            name='id',
            field=models.BigAutoField(db_index=True, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='abstractproductmeta',
            name='id',
            field=models.BigAutoField(db_index=True, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='abstractproductside',
            name='id',
            field=models.BigAutoField(db_index=True, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='abstractproductvariant',
            name='id',
            field=models.BigAutoField(db_index=True, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='abstractproductvariantattribute',
            name='id',
            field=models.BigAutoField(db_index=True, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='categoryproduct',
            name='id',
            field=models.BigAutoField(db_index=True, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='id',
            field=models.BigAutoField(db_index=True, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='productattributevalue',
            name='id',
            field=models.BigAutoField(db_index=True, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='productsideimages',
            name='id',
            field=models.BigAutoField(db_index=True, primary_key=True, serialize=False, unique=True),
        ),
    ]
