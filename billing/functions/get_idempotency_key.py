from HUB import settings


def get_idempotency_key(invoice_id, previous_keys=None):
    increment_key = 0
    base_key = f'{settings.IDEMPOTENCY_KEY_PREFIX}{invoice_id}'
    if previous_keys is None or len(previous_keys) == 0:
        return base_key
    key = base_key
    while True:
        if key in previous_keys:
            increment_key += 1
            key = f'{base_key}_{increment_key}'
        else:
            break
    return key
