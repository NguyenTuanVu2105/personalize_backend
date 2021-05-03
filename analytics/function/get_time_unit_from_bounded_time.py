from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.db.models.functions import TruncHour, TruncDate, TruncMonth, TruncQuarter

from analytics.constants.statistic_unit import StatisticUnit


def get_time_unit_from_bounded_time(since, until):
    day_timedelta = (until - since) / timedelta(days=1)

    if day_timedelta <= 1:
        statistic_unit = StatisticUnit.hour
        extract_time_func = TruncHour
        one_unit_time_delta = timedelta(hours=1)
        time_format = "%Y-%m-%d %H:00:00"
    elif day_timedelta <= 31:
        statistic_unit = StatisticUnit.day
        extract_time_func = TruncDate
        one_unit_time_delta = timedelta(days=1)
        time_format = "%Y-%m-%d"
    elif day_timedelta <= 365:
        statistic_unit = StatisticUnit.month
        extract_time_func = TruncMonth
        one_unit_time_delta = relativedelta(months=1)
        time_format = "%Y-%m"
    else:
        statistic_unit = StatisticUnit.quarter
        extract_time_func = TruncQuarter
        one_unit_time_delta = relativedelta(months=3)
        time_format = "%Y-#Q"
    return statistic_unit, extract_time_func, one_unit_time_delta, time_format
