class CeleryTask:
    SCHEDULED_CHECK_ORDER = "scheduled_check_order"
    SCHEDULED_MERGE_INVOICE = "scheduled_merge_invoice"
    SCHEDULED_TASK_AUTO_CHARGING = "scheduled_task_auto_charging"
    SCHEDULED_TASK_AUTO_CHECK_TRANSACTION_PENDING_INVOICE = "scheduled_task_auto_check_transaction_pending_invoice"
    SCHEDULED_TASK_AUTO_CHECK_LONG_INVOICE_PROCESSING = "scheduled_task_auto_check_long_invoice_processing"
    SCHEDULED_TASK_AUTO_REFUND = "scheduled_task_auto_refund"
    SCHEDULED_AUTO_SCAN_PAID_ORDERS = "scheduled_auto_scan_paid_orders"
    SCHEDULED_AUTO_SCAN_TO_PREPARE_TO_CHARGE_ORDERS = "scheduled_auto_scan_to_prepare_to_charge_orders"
    SCHEDULED_AUTO_SCAN_TO_PUSH_ORDERS_TO_FULFILL = "scheduled_auto_scan_to_push_orders_to_fulfill"
    SCHEDULED_UPDATE_CURRENCY_EXCHANGE_RATES = "scheduled_update_currency_exchange_rates"
    SCHEDULED_ORDER_PACK_TRACKING_SCANS = "scheduled_order_pack_tracking_scans"
    SCHEDULED_ORDER_PACK_UNKNOWN_TRACKING_SCAN = "scheduled_order_pack_unknown_tracking_scan"
    SCHEDULED_AUTO_CLEAR_MAIL_HISTORY = "scheduled_auto_clear_mail_history"
    SCHEDULED_AUTO_REMOVE_INVALID_PAYEE_IDS = "scheduled_auto_remove_invalid_payee_ids"
    SCHEDULED_REMOVE_OLD_RATE_LIMIT_SEQS = "scheduled_remove_old_rate_limit_seqs"
    SCHEDULED_AUTO_SCAN_SUPPORT_TICKET = "scheduled_auto_scan_support_ticket"
    SCHEDULED_SCAN_PENDING_WEBHOOK_JOB = "scheduled_scan_pending_webhook_job"
    SCHEDULED_RENEW_PAYPAL_ACCESS_TOKEN = "scheduled_renew_paypal_access_token"
    SCHEDULED_DELETE_UNUSED_ARTWORK = "scheduled_delete_unused_artwork"
    SCHEDULED_CLEAN_REFRESH_TOKEN = "scheduled_clean_refresh_token"
    TASK_RENEW_PAYPAL_ACCESS_TOKEN = "task_renew_paypal_access_token"
    TASK_SEND_NOTIFICATION = "task_send_notification"
    TASK_SEND_ADMIN_NOTIFICATION = "task_send_admin_notification"
    TASK_SEND_ACTIVATION_EMAIL = "task_send_activation_email"
    TASK_SEND_WARNING_AUTHENICATION = "task_send_warning_authenication"
    TASK_SEND_WELCOME_USER_EMAIL = "task_send_welcome_user_email"
    TASK_CREATE_USER_VARIANT_DEFAULT_PRICE = "task_create_user_variant_default_price"
    TASK_GENERATE_PRODUCT_ARTWORK_FUSIONS = "task_generate_product_artwork_fusions"
    TASK_SYNC_SHOP_USER_PRODUCT_FROM_OTHERS = "task_sync_shop_user_product_from_others"
    TASK_PROCESS_PRODUCT_MOCKUP = "task_process_product_mockup"
    TASK_UPDATE_FULFILL_ARTWORK = "task_update_fulfill_artwork"
    TASK_CREATE_PRODUCT_IN_SHOP = "task_create_product_in_shop"
    TASK_UPDATE_PRODUCT_IN_SHOP = "task_update_product_in_shop"
    TASK_UPDATE_ALL_PRODUCT_IN_SHOP = "task_update_all_product_in_shop"
    TASK_UPDATE_USER_PRODUCT_IN_ALL_SHOP = "task_update_user_product_in_all_shop"
    TASK_CHARGE_INVOICE = "task_charge_invoice"
    TASK_UPDATE_ORDER_SUPPORT_TICKET_INFO = "task_update_order_support_ticket_info"
    TASK_BULK_RESYNC_PRODUCT = "bulk_resync_product_task"
    TASK_SEND_FORGOT_PASSWORD_MAIL = "send_forgot_password_mail_task"
    TASK_RUN_WEBHOOK_JOB_FULFILLMENT_ORDER = "task_run_webhook_job_fulfillment_order"
    TASK_RUN_WEBHOOK_JOB_FULFILLMENT_PRODUCT = "task_run_webhook_job_fulfillment_product"
    TASK_RUN_WEBHOOK_JOB_ADAPTER_ORDER = "task_run_webhook_job_adapter_order"
    TASK_RUN_WEBHOOK_JOB_ADAPTER_PRODUCT = "task_run_webhook_job_adapter_product"
    TASK_RUN_WEBHOOK_JOB_EX_ADAPTER_SHOP_USER_PRODUCT_FROM_OTHERS = "task_run_webhook_job_ex_adapter_shop_user_product_from_others"
    TASK_RUN_WEBHOOK_JOB_MOCKUP_ARTWORK_FUSION = "task_run_webhook_job_mockup_artwork_fusion"
    TASK_RUN_WEBHOOK_JOB_ADAPTER_APP = "task_run_webhook_job_adapter_app"
    TASK_PROCESS_NO_ARTWORK_PRODUCT = "process_no_artwork_product"
    TASK_UPDATE_ORDER_CACHED_METADATA = "task_update_order_cached_metadata"
    TASK_UPDATE_TICKET_CONVERSATION = "task_update_ticket_conversation"
    TASK_DELETE_USER_PRODUCT_IN_SHOP = "task_delete_user_product_in_shop"
    SCHEDULED_INIT_CACHE_PRODUCTS = "scheduled_init_cache_products"
    TASK_CACHE_ABSTRACT_CATEGORY_PRODUCTS = "task_cache_abstract_category_products"
    TASK_CACHE_ABSTRACT_PRODUCT = "task_cache_abstract_product"
    TASK_DELETE_USER_PRODUCT_IN_MULTIPLE_SHOP = "task_delete_user_product_in_multiple_shop"
    TASK_CACHE_OBJECT_IF_NOT_EXIST = "task_cache_object_if_not_exist"
    SCHEDULED_CALCULATE_ARTWORK_USED_TIME = "scheduled_calculate_artwork_used_time"
    TASK_CREATE_USER_VARIANT_PRICES = "task_create_user_variant_prices"
    TASK_SEND_CREATED_ACCOUNT_EMAIL = "task_send_created_account_email"
    SCHEDULED_UPDATE_PRODUCTION_STATISTIC = "scheduled_update_production_statistic"
    SCHEDULED_UPDATE_SHIPPING_TIME_STATISTIC = "scheduled_update_shipping_time_statistic"
    SCHEDULED_TASK_AUTO_CHECK_INCOMING_WEBHOOK = "scheduled_task_auto_check_incoming_webhook"
    TASK_UPDATE_USER_GEOLOCATION = 'task_update_user_geolocation'
    TASK_CREATE_ORDER_SHIPPING_NOTIFICATION = 'task_create_order_shipping_notification'
    TASK_CREATE_ORDER_DELIVERED_NOTIFICATION = 'task_create_order_delivered_notification'
    TASK_CREATE_ORDER_REVIEW_MAIL = 'task_create_order_review_mail'
    TASK_CREATE_ADD_PAYMENT_MAIL = 'task_create_add_payment_mail'
    SCHEDULED_SEND_ORDER_TRACKING_NOTIFICATION = 'scheduled_send_order_tracking_notification'
    TASK_RUN_WEBHOOK_JOB_ADAPTER_SHOP = 'task_run_webhook_job_adapter_shop'
    TASK_SEND_SELLER_CUSTOM_EMAIL = 'task_send_seller_custom_email'
    TASK_CREATE_SERVICE_COMMUNICATION_LOG = 'task_create_service_communication_log'
    SCHEDULED_AUTO_SCAN_DELIVER_ORDER = 'scheduled_auto_scan_delivered_order'
    SCHEDULED_AUTO_SCAN_AND_SEND_REVIEW_MAIL = 'scheduled_auto_scan_and_send_review_mail'
    SCHEDULED_AUTO_SCAN_AND_SEND_ADD_PAYMENT_MAIL = 'scheduled_auto_scan_and_send_add_payment_mail'
    SCHEDULED_DELETE_UNUSED_MOCKUPS = 'scheduled_delete_unused_mockups'


ALL_TASKS = [
    CeleryTask.SCHEDULED_CHECK_ORDER,
    CeleryTask.SCHEDULED_MERGE_INVOICE,
    CeleryTask.SCHEDULED_TASK_AUTO_CHARGING,
    CeleryTask.SCHEDULED_TASK_AUTO_CHECK_TRANSACTION_PENDING_INVOICE,
    CeleryTask.SCHEDULED_TASK_AUTO_CHECK_LONG_INVOICE_PROCESSING,
    CeleryTask.SCHEDULED_TASK_AUTO_REFUND,
    CeleryTask.SCHEDULED_AUTO_SCAN_PAID_ORDERS,
    CeleryTask.SCHEDULED_AUTO_SCAN_TO_PREPARE_TO_CHARGE_ORDERS,
    CeleryTask.SCHEDULED_AUTO_SCAN_TO_PUSH_ORDERS_TO_FULFILL,
    CeleryTask.SCHEDULED_UPDATE_CURRENCY_EXCHANGE_RATES,
    CeleryTask.SCHEDULED_ORDER_PACK_TRACKING_SCANS,
    CeleryTask.SCHEDULED_AUTO_CLEAR_MAIL_HISTORY,
    CeleryTask.SCHEDULED_AUTO_REMOVE_INVALID_PAYEE_IDS,
    CeleryTask.SCHEDULED_REMOVE_OLD_RATE_LIMIT_SEQS,
    CeleryTask.SCHEDULED_AUTO_SCAN_SUPPORT_TICKET,
    CeleryTask.SCHEDULED_SCAN_PENDING_WEBHOOK_JOB,
    CeleryTask.SCHEDULED_RENEW_PAYPAL_ACCESS_TOKEN,
    CeleryTask.SCHEDULED_DELETE_UNUSED_ARTWORK,
    CeleryTask.SCHEDULED_CLEAN_REFRESH_TOKEN,
    CeleryTask.TASK_SEND_NOTIFICATION,
    CeleryTask.TASK_SEND_ADMIN_NOTIFICATION,
    CeleryTask.TASK_SEND_ACTIVATION_EMAIL,
    CeleryTask.TASK_SEND_WARNING_AUTHENICATION,
    CeleryTask.TASK_SEND_WELCOME_USER_EMAIL,
    CeleryTask.TASK_CREATE_USER_VARIANT_DEFAULT_PRICE,
    CeleryTask.TASK_GENERATE_PRODUCT_ARTWORK_FUSIONS,
    CeleryTask.TASK_PROCESS_PRODUCT_MOCKUP,
    CeleryTask.TASK_UPDATE_FULFILL_ARTWORK,
    CeleryTask.TASK_CREATE_PRODUCT_IN_SHOP,
    CeleryTask.TASK_UPDATE_PRODUCT_IN_SHOP,
    CeleryTask.TASK_UPDATE_ALL_PRODUCT_IN_SHOP,
    CeleryTask.TASK_UPDATE_USER_PRODUCT_IN_ALL_SHOP,
    CeleryTask.TASK_UPDATE_ORDER_SUPPORT_TICKET_INFO,
    CeleryTask.TASK_BULK_RESYNC_PRODUCT,
    CeleryTask.TASK_SEND_FORGOT_PASSWORD_MAIL,
    CeleryTask.TASK_SEND_FORGOT_PASSWORD_MAIL,
    CeleryTask.TASK_SYNC_SHOP_USER_PRODUCT_FROM_OTHERS,
    CeleryTask.TASK_RUN_WEBHOOK_JOB_FULFILLMENT_PRODUCT,
    CeleryTask.TASK_RUN_WEBHOOK_JOB_FULFILLMENT_ORDER,
    CeleryTask.TASK_RUN_WEBHOOK_JOB_ADAPTER_PRODUCT,
    CeleryTask.TASK_RUN_WEBHOOK_JOB_ADAPTER_ORDER,
    CeleryTask.TASK_RUN_WEBHOOK_JOB_EX_ADAPTER_SHOP_USER_PRODUCT_FROM_OTHERS,
    CeleryTask.TASK_RUN_WEBHOOK_JOB_MOCKUP_ARTWORK_FUSION,
    CeleryTask.TASK_PROCESS_NO_ARTWORK_PRODUCT,
    CeleryTask.TASK_UPDATE_ORDER_CACHED_METADATA,
    CeleryTask.TASK_UPDATE_TICKET_CONVERSATION,
    CeleryTask.TASK_UPDATE_TICKET_CONVERSATION,
    CeleryTask.TASK_RENEW_PAYPAL_ACCESS_TOKEN,
    CeleryTask.TASK_DELETE_USER_PRODUCT_IN_SHOP,
    CeleryTask.TASK_CACHE_ABSTRACT_CATEGORY_PRODUCTS,
    CeleryTask.TASK_CACHE_ABSTRACT_PRODUCT,
    CeleryTask.SCHEDULED_INIT_CACHE_PRODUCTS,
    CeleryTask.TASK_DELETE_USER_PRODUCT_IN_MULTIPLE_SHOP,
    CeleryTask.TASK_CACHE_OBJECT_IF_NOT_EXIST,
    CeleryTask.SCHEDULED_CALCULATE_ARTWORK_USED_TIME,
    CeleryTask.TASK_CREATE_USER_VARIANT_PRICES,
    CeleryTask.TASK_SEND_CREATED_ACCOUNT_EMAIL,
    CeleryTask.TASK_RUN_WEBHOOK_JOB_ADAPTER_APP,
    CeleryTask.SCHEDULED_UPDATE_PRODUCTION_STATISTIC,
    CeleryTask.SCHEDULED_UPDATE_SHIPPING_TIME_STATISTIC,
    CeleryTask.SCHEDULED_TASK_AUTO_CHECK_INCOMING_WEBHOOK,
    CeleryTask.SCHEDULED_ORDER_PACK_UNKNOWN_TRACKING_SCAN,
    CeleryTask.TASK_UPDATE_USER_GEOLOCATION,
    CeleryTask.TASK_CREATE_ORDER_SHIPPING_NOTIFICATION,
    CeleryTask.TASK_CREATE_ORDER_DELIVERED_NOTIFICATION,
    CeleryTask.SCHEDULED_SEND_ORDER_TRACKING_NOTIFICATION,
    CeleryTask.TASK_RUN_WEBHOOK_JOB_ADAPTER_SHOP,
    CeleryTask.TASK_SEND_SELLER_CUSTOM_EMAIL,
    CeleryTask.TASK_CREATE_SERVICE_COMMUNICATION_LOG,
    CeleryTask.SCHEDULED_AUTO_SCAN_DELIVER_ORDER,
    CeleryTask.SCHEDULED_AUTO_SCAN_AND_SEND_REVIEW_MAIL,
    CeleryTask.SCHEDULED_AUTO_SCAN_AND_SEND_ADD_PAYMENT_MAIL,
    CeleryTask.SCHEDULED_DELETE_UNUSED_MOCKUPS,
    CeleryTask.TASK_CREATE_ADD_PAYMENT_MAIL,
    CeleryTask.TASK_CREATE_ORDER_REVIEW_MAIL
]

CELERY_TASK_ROUTES = dict(map(lambda task: (task, {"queue": task}), ALL_TASKS + [CeleryTask.TASK_CHARGE_INVOICE]))

CELERY_TASK_QUEUES = dict(map(lambda task: (task, {"exchange": task, "binding_key": "default"}), ALL_TASKS))
