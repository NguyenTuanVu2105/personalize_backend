from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('notification', '0063_auto_20210319_1515'),
    ]

    operations = [
        migrations.RunSQL(
        	"""
        		
        	"""
            'INSERT INTO public.notification_template (type, message_title, message_content, mail_title, mail_content, send_email, send_message, parameter_list) VALUES '
            + '(\'24\', \'\', \'\', \'Please Add Payment And Recharge Order\', \'Hi {user_name}, Please Add Payment And Recharge Order {order_id}\', true, false, \' \')'
        ),
    ]