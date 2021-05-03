from django.db import models



class MailSetting(models.Model):
    admin_mail = models.CharField(max_length=255)
    is_send_mail_user = models.BooleanField(default=False)
    send_order_mail_start_time = models.DateTimeField(null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        db_table = 'mail_setting'