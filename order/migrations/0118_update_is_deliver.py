from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0117_merge_20210323_0456'),
    ]

    operations = [
        migrations.RunSQL("UPDATE public.order SET is_delivered_order = true WHERE is_delivered_order is null")
    ]