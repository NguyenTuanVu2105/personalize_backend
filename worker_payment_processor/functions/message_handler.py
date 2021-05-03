import json
import logging

from billing.constants.transaction_statuses import TransactionStatus
from worker_payment_processor.exceptions.duplicate_charge_exception import DuplicateChargeException
from worker_payment_processor.functions.charge_invoice import charge_invoice
from worker_payment_processor.functions.check_invoice import check_invoice
from worker_payment_processor.functions.update_invoice import update_invoice

logger = logging.getLogger(__name__)


def message_handle(channel, method_frame, header_frame, body):
    logger.info(json.loads(body.decode('utf-8')))
    invoice_info = json.loads(json.loads(body.decode('utf-8'))[0][0])
    invoice_id = invoice_info['invoice_id']
    charge_count = invoice_info['charge_count']
    # ---- CHECK INVOICE ---
    try:
        invoice_process_info = check_invoice(invoice_id, charge_count)
    except DuplicateChargeException:
        logger.info("Duplicated charge")
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        return
    except Exception as e:
        logger.exception(e)
        channel.basic_reject(delivery_tag=method_frame.delivery_tag, requeue=True)
        return
    else:
        logger.info(f"ACKED {invoice_id}")
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    # ---- CHARGE INVOICE ---
    try:
        charge_status, transactions = charge_invoice(invoice_process_info)
    except Exception as e:
        logger.exception(e)
        charge_status = TransactionStatus.TRANSACTION_PENDING
        transactions = []

    # ---- UPDATE INVOICE ---
    try:
        update_invoice(invoice_process_info, charge_status, transactions)
    except Exception as e:
        logger.exception(e)
