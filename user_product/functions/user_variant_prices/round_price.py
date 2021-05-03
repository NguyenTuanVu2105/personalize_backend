import logging
from decimal import Decimal
from math import ceil

logger = logging.getLogger(__name__)


def round_price(price, precision):
    if precision < 0:
        round_degree = pow(10, Decimal(precision))
        return ceil(price * round_degree) / round_degree
    else:
        return round(price, precision)


def change_precision(precision):
    return precision if precision > 0 else 0


