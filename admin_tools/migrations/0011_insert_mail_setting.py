from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('admin_tools', '0010_mailsetting'),
    ]

    operations = [
        migrations.RunSQL(
            'INSERT INTO public.mail_setting (admin_mail, is_send_mail_user, create_time, update_time) VALUES '
            + "('printholo.test003@gmail.com', False, current_timestamp, current_timestamp);"
        ),
    ]