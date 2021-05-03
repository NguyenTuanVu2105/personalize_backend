from order.models import Order
from service_communication.constants.incoming_webhook_statuses import IncomingWebhookStatus
from service_communication.constants.incoming_webhook_types import IncomingWebhookType
from service_communication.models import IncomingWebhook

success_status = 'success'
failed_status = 'failed'
skipped_status = 'skipped'


def bulk_update_order_mfr_cost():
    hooks = IncomingWebhook.objects.filter(type=IncomingWebhookType.FULFILL_PROCESS_ORDER,
                                           status=IncomingWebhookStatus.RESOLVED).order_by('-update_time',
                                                                                           '-create_time')
    response_dict = {}
    for hook in hooks:
        status, data = update_order_mfr_cost(hook)
        if status not in response_dict:
            response_dict[status] = [data, ]
        else:
            response_dict[status].append(data)
    return response_dict


def update_order_mfr_cost(hook):
    try:
        order = Order.objects.get(id=hook.object_id)
        if order.total_mfr_cost is not None:
            return skipped_status, {
                'order_id': order.id
            }
        data = hook.body_data
        fulfillments = data.get('fulfillments')
        full_order_cost = sum([(fulfillment.get('shipping_cost') or 0) + sum(
            [float(item.get('total_cost') or '0')
             for item in (fulfillment.get('items') or [])]
        ) for fulfillment in fulfillments])
        order.total_mfr_cost = full_order_cost
        order.save()
        return success_status, {
            'order_id': order.id,
            'success': True,
            'cost': full_order_cost
        }
    except Exception as e:
        return failed_status, {
            'order_id': hook.object_id,
            'success': False,
            'error': str(e)
        }
