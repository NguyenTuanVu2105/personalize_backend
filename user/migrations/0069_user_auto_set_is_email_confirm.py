from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0068_user_is_lock'),
    ]

    operations = [
        migrations.RunSQL(
            """
            UPDATE "user" SET is_email_confirmed = True WHERE 1=1;
            """
        )
    ]