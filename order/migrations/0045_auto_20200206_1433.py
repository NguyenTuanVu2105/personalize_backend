# Generated by Django 2.2.2 on 2020-02-03 17:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0044_auto_20200203_1705'),
    ]

    operations = [
        migrations.RunSQL(
            [('INSERT INTO "public"."notification_template" ("type", "message_title", "message_content", "mail_title", "mail_content", "send_email", "send_message", "parameter_list") VALUES (%s, %s, %s, %s, %s, true , false , %s);COMMIT;', ["9", "", "", "[Order Support] - Order: #{order_id} - {subject}",
                                                                                                                                                                                                                                                 "<table role=\'presentation\' border=\'0\' cellpadding=\'0\' cellspacing=\'0\' class=\'body\'> <tr> <td> </td> <td class=\'container\'> <div class=\'content\'> <table role=\'presentation\' class=\'main\'> <tr> <td class=\'wrapper\'> <table role=\'presentation\' border=\'0\' cellpadding=\'0\' cellspacing=\'0\'> <tr> <td> <p>Hi there,</p> <p>At {time}, you sent us an issue about order {order_id}, store {store_name}. Below is your issue content:</p> <em>\"{content}\"</em> <p>This issue was forwarded to our support team and they will response to you as soon as possible. Thank you for this contact.</p> <p>All the best, </p> <p>PrintHolo team</p> </td> </tr> </table> </td> </tr> </table>",
                                                                                                                                                                                                                                                 "time: time sent issue, order_id: id of order, content: content of issue"])],
        ),
        migrations.RunSQL(
            [('INSERT INTO "public"."notification_template" ("type", "message_title", "message_content", "mail_title", "mail_content", "send_email", "send_message", "parameter_list") VALUES (%s, %s, %s, %s, %s, true , false , %s);COMMIT;', ["10", "", "", "[Order Support] - Order: #{order_id} - {subject}",
                                                                                                                                                                                                                                                 "<table role=\'presentation\' border=\'0\' cellpadding=\'0\' cellspacing=\'0\' class=\'body\'> <tr> <td> </td> <td class=\'container\'> <div class=\'content\'> <table role=\'presentation\' class=\'main\'> <tr> <td class=\'wrapper\'> <table role=\'presentation\' border=\'0\' cellpadding=\'0\' cellspacing=\'0\'> <tr> <td> <p>Hi there,</p> <p>At {time}, seller {seller} sent us an issue about order {order_id}, store {store_name}. Below is him/her issue content:</p> <em>\"{content}\"</em> <p>Please read carefully this isue and response to him/her.</p> <p>All the best, </p> <p>PrintHolo system</p> </td> </tr> </table> </td> </tr> </table>",
                                                                                                                                                                                                                                                 "time: time sent issue, seller: seller name, order_id: id of order, content: content of issue"])]
        ),
    ]
