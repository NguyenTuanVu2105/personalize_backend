def parse_order_ids(order_ids):
    str = ''
    for order in order_ids:
        str += '#{}, '.format(order)
    return str[:-2]