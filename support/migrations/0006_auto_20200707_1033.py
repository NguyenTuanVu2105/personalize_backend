# Generated by Django 2.2.2 on 2020-07-07 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0005_supportticket_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supporttickettarget',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='targets', to='support.SupportTicket'),
        ),
    ]
