# Generated by Django 2.2.2 on 2021-03-12 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0057_insert_email_template_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailhistory',
            name='type',
            field=models.CharField(blank=True, choices=[('0', 'cancel_shipping_approved'), ('1', 'cancel_shipping_rejected'), ('2', 'registration_activation_email'), ('3', 'add_payment_prompt'), ('4', 'recharge_notification'), ('5', 'cancel_order_success'), ('6', 'cancel_order_success_shop_owner'), ('7', 'order_rejected'), ('8', 'order_rejected_shop_owner'), ('9', 'seller_order_contact_support'), ('11', 'admin_refund_failed'), ('12', 'admin_long_invoice_processing'), ('13', 'forgot_password_email'), ('14', 'ticket_resolved'), ('15', 'user_product_delete'), ('16', 'order_shipping_address_update_rejected'), ('17', 'create_account_by_email'), ('18', 'order_shipping_notification'), ('19', 'order_delivered_notification'), ('20', 'warning_authenication'), ('21', 'welcome_user'), ('22', 'unprofitable_order'), ('23', 'order_delivered_review')], default='0', max_length=2),
        ),
        migrations.AlterField(
            model_name='message',
            name='type',
            field=models.CharField(blank=True, choices=[('0', 'cancel_shipping_approved'), ('1', 'cancel_shipping_rejected'), ('2', 'registration_activation_email'), ('3', 'add_payment_prompt'), ('4', 'recharge_notification'), ('5', 'cancel_order_success'), ('6', 'cancel_order_success_shop_owner'), ('7', 'order_rejected'), ('8', 'order_rejected_shop_owner'), ('9', 'seller_order_contact_support'), ('11', 'admin_refund_failed'), ('12', 'admin_long_invoice_processing'), ('13', 'forgot_password_email'), ('14', 'ticket_resolved'), ('15', 'user_product_delete'), ('16', 'order_shipping_address_update_rejected'), ('17', 'create_account_by_email'), ('18', 'order_shipping_notification'), ('19', 'order_delivered_notification'), ('20', 'warning_authenication'), ('21', 'welcome_user'), ('22', 'unprofitable_order'), ('23', 'order_delivered_review')], default='0', max_length=2),
        ),
        migrations.AlterField(
            model_name='template',
            name='type',
            field=models.CharField(blank=True, choices=[('0', 'cancel_shipping_approved'), ('1', 'cancel_shipping_rejected'), ('2', 'registration_activation_email'), ('3', 'add_payment_prompt'), ('4', 'recharge_notification'), ('5', 'cancel_order_success'), ('6', 'cancel_order_success_shop_owner'), ('7', 'order_rejected'), ('8', 'order_rejected_shop_owner'), ('9', 'seller_order_contact_support'), ('11', 'admin_refund_failed'), ('12', 'admin_long_invoice_processing'), ('13', 'forgot_password_email'), ('14', 'ticket_resolved'), ('15', 'user_product_delete'), ('16', 'order_shipping_address_update_rejected'), ('17', 'create_account_by_email'), ('18', 'order_shipping_notification'), ('19', 'order_delivered_notification'), ('20', 'warning_authenication'), ('21', 'welcome_user'), ('22', 'unprofitable_order'), ('23', 'order_delivered_review')], default='0', max_length=2, primary_key=True, serialize=False),
        ),
    ]
