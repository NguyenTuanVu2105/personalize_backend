# Generated by Django 2.2.2 on 2021-04-16 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_product', '0141_auto_20210409_1131'),
        ('user', '0072_usersettings_default_branding_card_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersettings',
            name='default_branding_card_id',
        ),
        migrations.AddField(
            model_name='usersettings',
            name='default_branding_card',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_product.UserProduct'),
        ),
    ]
