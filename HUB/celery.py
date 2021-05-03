from __future__ import absolute_import, unicode_literals

import logging
import os
from datetime import timedelta

import django
from celery import Celery
from django.conf import settings

from HUB.celery_modules.celery_shedule_task import decorate_app_schedule_task, Task
from HUB.constants.celery_task import CeleryTask, CELERY_TASK_ROUTES, CELERY_TASK_QUEUES

# set the default Django settings module for the 'celery' program.
# from HUB.settings.celery_setting import CeleryTask, CELERY_TASK_ROUTES

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HUB.settings')
# Setup django project
# django.setup()
app = Celery('HUB', task_cls=Task)
django.setup()

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.task_routes = CELERY_TASK_ROUTES
app.conf.task_queues = CELERY_TASK_QUEUES
logger = logging.getLogger(__name__)

app.conf.beat_schedule = {
    # Disable cleanup task by scheduling to run every ~1000 years
    'celery.backend_cleanup': {
        'task': 'celery.backend_cleanup',
        'schedule': timedelta(days=365 * 1000),
        'relative': True,
    },
}

schedule_task_decorator = decorate_app_schedule_task(app)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # check_order
    sender.add_periodic_task(1 * 60, check_order.s())

    # merge invoice
    sender.add_periodic_task(30, merge_invoice.s())

    # autopay
    sender.add_periodic_task(5, task_auto_charging.s())

    # auto check pending transaction
    sender.add_periodic_task(30 * 60, task_auto_check_transaction_pending_invoice.s())

    # auto check long processing
    sender.add_periodic_task(15 * 60, task_auto_check_long_invoice_processing.s())

    # # auto scan completely paid order
    # sender.add_periodic_task(1 * 60, auto_scan_paid_orders.s())

    # auto scan new order for fulfillment
    sender.add_periodic_task(15, auto_scan_to_prepare_to_charge_orders.s())

    # auto scan new order for fulfillment
    sender.add_periodic_task(15, auto_scan_to_push_orders_to_fulfill.s())

    # auto_refund
    sender.add_periodic_task(30, task_auto_refund.s())

    # update currency
    sender.add_periodic_task(30 * 60, update_currency_exchange_rates.s())

    # update tracking
    sender.add_periodic_task(3 * 60, order_pack_tracking_scan.s())

    # update unknown tracking
    sender.add_periodic_task(6 * 60, order_pack_unknown_tracking_scan.s())

    # clear mail history
    sender.add_periodic_task(24 * 60 * 60, auto_clear_mail_history.s())

    # Payoneer remove invalid payee
    sender.add_periodic_task(24 * 60 * 60, auto_remove_invalid_payee_ids.s())

    # remove invalid payee
    sender.add_periodic_task(1 * 60 * 60, remove_old_rate_limit_seqs.s())

    # scan support tickets
    sender.add_periodic_task(1 * 20, auto_scan_support_ticket.s())

    # scan pending webhook jobs
    sender.add_periodic_task(1 * 5, auto_scan_pending_webhook_job.s())

    # auto cache abstract product by category
    # sender.add_periodic_task(60 * 60 * 24, auto_cache_abstract_products.s())

    # check paypal token each 30min (constraints with timer inside original function)
    sender.add_periodic_task(1 * 1800, auto_check_paypal_token_expiration.s())

    # delete unused artworks
    sender.add_periodic_task(60 * 60, auto_delete_unused_artworks.s())

    # calculate artwork used time
    sender.add_periodic_task(60 * 60, auto_calculate_artwork_used_time.s())

    # clean refresh token in database: per 7days
    sender.add_periodic_task(60 * 60 * 24 * 2, auto_clean_refresh_token_in_db.s())
    # sender.add_periodic_task(60, auto_clean_refresh_token_in_db.s())

    # update production statistic
    sender.add_periodic_task(24 * 60 * 60, auto_update_production_statistic.s())

    # update shipping time statistic
    sender.add_periodic_task(24 * 60 * 60, auto_update_shipping_time_statistic.s())

    # send order tracking notification
    sender.add_periodic_task(4 * 60 * 60, scheduled_send_order_tracking_notification.s())

    # auto scan order deliver
    sender.add_periodic_task(4 * 60 * 60, auto_scan_order_deliver.s())

    # auto scan and send review mail
    sender.add_periodic_task(4 * 60 * 60, auto_scan_and_send_review_mail.s())

    # auto scan and send add payment mail
    sender.add_periodic_task(1 * 60 * 60, auto_scan_and_send_add_payment_mail.s())

    # auto delete unused mockups
    sender.add_periodic_task(12 * 60 * 60, scheduled_delete_unused_mockups.s())


@schedule_task_decorator(name=CeleryTask.SCHEDULED_CHECK_ORDER)
def check_order():
    try:
        from order.services import check_all_shop_order
        check_all_shop_order()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_MERGE_INVOICE)
def merge_invoice():
    from billing.services import InvoiceService
    InvoiceService.create_invoice()


@schedule_task_decorator(name=CeleryTask.SCHEDULED_TASK_AUTO_CHARGING)
def task_auto_charging():
    try:
        from billing.sub_apps.combine_payment.functions import auto_charging
        return auto_charging()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_TASK_AUTO_CHECK_TRANSACTION_PENDING_INVOICE)
def task_auto_check_transaction_pending_invoice():
    try:
        from billing.sub_apps.combine_payment.functions.check_transaction_pending_charge import \
            TransactionPendingChecker
        TransactionPendingChecker.auto_check_transaction_pending_invoice()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_TASK_AUTO_CHECK_LONG_INVOICE_PROCESSING)
def task_auto_check_long_invoice_processing():
    try:
        from billing.sub_apps.combine_payment.functions.check_long_processing_charge import \
            auto_check_long_invoice_processing
        auto_check_long_invoice_processing()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_TASK_AUTO_REFUND)
def task_auto_refund():
    try:
        from billing.sub_apps.combine_payment.functions import auto_refund
        auto_refund()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_AUTO_SCAN_TO_PREPARE_TO_CHARGE_ORDERS)
def auto_scan_to_prepare_to_charge_orders():
    try:
        from order.services.service_order import scan_to_prepare_to_charge_orders
        scan_to_prepare_to_charge_orders()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_AUTO_SCAN_TO_PUSH_ORDERS_TO_FULFILL)
def auto_scan_to_push_orders_to_fulfill():
    try:
        from order.services.service_order import scan_to_push_orders_to_fulfill
        scan_to_push_orders_to_fulfill()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_UPDATE_CURRENCY_EXCHANGE_RATES)
def update_currency_exchange_rates():
    try:
        from system_metadata.services import update_all_currency_ex_rates
        update_all_currency_ex_rates()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_ORDER_PACK_TRACKING_SCANS)
def order_pack_tracking_scan():
    try:
        from order.services.order_pack_tracking_scan import check_all_order_pack_tracking
        check_all_order_pack_tracking()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_ORDER_PACK_UNKNOWN_TRACKING_SCAN)
def order_pack_unknown_tracking_scan():
    try:
        from order.services.order_pack_tracking_scan import check_all_unknown_tracking
        check_all_unknown_tracking()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_AUTO_CLEAR_MAIL_HISTORY)
def auto_clear_mail_history():
    try:
        from notification.services.service_mail_history import clear_mail_history
        clear_mail_history()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_AUTO_REMOVE_INVALID_PAYEE_IDS)
def auto_remove_invalid_payee_ids():
    try:
        from billing.sub_apps.payoneer_payment.services.payoneer_payee_service import remove_invalid_payee_ids
        remove_invalid_payee_ids()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_REMOVE_OLD_RATE_LIMIT_SEQS)
def remove_old_rate_limit_seqs():
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute('select clear_rate_limit()')
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_AUTO_SCAN_SUPPORT_TICKET)
def auto_scan_support_ticket():
    try:
        from support.function.scan_tickets_by_time import scan_tickets_by_time
        scan_tickets_by_time()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_SCAN_PENDING_WEBHOOK_JOB)
def auto_scan_pending_webhook_job():
    try:
        from service_communication.services.webhook_job_services.auto_run_webhook_job import \
            auto_run_all_pending_webhook_job
        auto_run_all_pending_webhook_job()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_RENEW_PAYPAL_ACCESS_TOKEN)
def auto_check_paypal_token_expiration():
    try:
        from billing.sub_apps.paypal_payment.services.paypal_authorization_services import PaypalAuthorizationService
        PaypalAuthorizationService.renew_access_token_from_db()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_DELETE_UNUSED_ARTWORK)
def auto_delete_unused_artworks():
    try:
        from user_product.functions import delete_unused_artworks
        delete_unused_artworks(self_delete=True)
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_INIT_CACHE_PRODUCTS)
def auto_cache_abstract_products():
    try:
        from abstract_product.tasks import cache_abstract_category_products_task
        from abstract_product.tasks import cache_abstract_products_task
        cache_abstract_category_products_task.delay()
        cache_abstract_products_task.delay()

    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_CALCULATE_ARTWORK_USED_TIME)
def auto_calculate_artwork_used_time():
    try:
        from user_product.functions import calculate_artwork_used_time
        calculate_artwork_used_time()

    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_CLEAN_REFRESH_TOKEN)
def auto_clean_refresh_token_in_db():
    try:
        from HUB.helpers.auth_helper import clean_refresh_token_in_db
        clean_refresh_token_in_db()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_UPDATE_PRODUCTION_STATISTIC)
def auto_update_production_statistic():
    try:
        from service_communication.services.fulfill_services.fulfill_statistic_communication_service import \
            FulfillStatisticCommunicationService
        from statistic.functions.update_from_dict import update_production_statistics
        response = FulfillStatisticCommunicationService.get_production_statistic()
        update_production_statistics(response['data'])
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_UPDATE_SHIPPING_TIME_STATISTIC)
def auto_update_shipping_time_statistic():
    try:
        from service_communication.services.fulfill_services.fulfill_statistic_communication_service import \
            FulfillStatisticCommunicationService
        from statistic.functions.update_from_dict import update_shipping_times
        response = FulfillStatisticCommunicationService.get_shipping_statistic()
        update_shipping_times(response['data'])
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_TASK_AUTO_CHECK_INCOMING_WEBHOOK)
def task_auto_long_process_incoming_webhook():
    try:
        from service_communication.services.incoming_webhook import auto_process_pending_incoming_webhooks
        return auto_process_pending_incoming_webhooks()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_SEND_ORDER_TRACKING_NOTIFICATION)
def scheduled_send_order_tracking_notification():
    try:
        from notification.services import handle_unsent_order_tracking_notification
        return handle_unsent_order_tracking_notification()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_AUTO_SCAN_DELIVER_ORDER)
def auto_scan_order_deliver():
    try:
        from order.tasks.scan_order_deliver import scan_order_deliver
        return scan_order_deliver()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_AUTO_SCAN_AND_SEND_REVIEW_MAIL)
def auto_scan_and_send_review_mail():
    try:
        from order.tasks.scan_and_send_mail_review_order import scan_and_send_mail_review_orders
        return scan_and_send_mail_review_orders()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_AUTO_SCAN_AND_SEND_ADD_PAYMENT_MAIL)
def auto_scan_and_send_add_payment_mail():
    try:
        from order.tasks.scan_and_send_mail_add_payment import scan_and_send_mail_add_payment
        return scan_and_send_mail_add_payment()
    except Exception as e:
        logger.exception(e)


@schedule_task_decorator(name=CeleryTask.SCHEDULED_DELETE_UNUSED_MOCKUPS)
def scheduled_delete_unused_mockups():
    try:
        from user_product.functions import delete_unused_mockups
        return delete_unused_mockups()
    except Exception as e:
        logger.exception(e)
