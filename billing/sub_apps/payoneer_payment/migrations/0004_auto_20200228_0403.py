# Generated by Django 2.2.2 on 2020-02-28 04:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('payoneer_payment', '0003_auto_20200211_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpayoneerpaymentmethod',
            name='payee_id',
            field=models.CharField(db_index=True, default='', max_length=30),
            preserve_default=False,
        ),
    ]
