from django.db import models



class CustomMailSender(models.Model):
    email = models.CharField(max_length=255)
    app_password = models.CharField(max_length=255)

    class Meta:
        db_table = 'mail_sender'