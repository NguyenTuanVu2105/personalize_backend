# Generated by Django 2.2.2 on 2021-01-07 09:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0102_auto_20210107_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordercomments',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ordercomments',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_comments', to='order.Order'),
        ),
    ]
