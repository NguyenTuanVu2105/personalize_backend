# Generated by Django 2.2.2 on 2020-07-20 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0013_auto_20200717_0644'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportticket',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
