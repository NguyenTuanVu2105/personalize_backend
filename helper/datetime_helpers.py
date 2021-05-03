from datetime import datetime, date

from django.utils import timezone


def get_current_datetime():
    return timezone.now()


def get_start_of_current_day_datetime():
    return get_current_datetime().replace(hour=0, minute=0, second=0, microsecond=0)


def naive_datetime_to_aware_datetime(naive_datetime):
    return timezone.make_aware(naive_datetime)


def get_quarter_from_month(month):
    assert isinstance(month, int)
    return (month - 1) // 3 + 1


def str_from_datetime(datetime_obj, datetime_format):
    assert isinstance(datetime_obj, (datetime, date))
    str_datetime = datetime_obj.strftime(datetime_format)
    quarter_directive = "#Q"
    if quarter_directive in datetime_format:
        str_quarter = "Q{}".format(get_quarter_from_month(datetime_obj.month))
        str_datetime = str_datetime.replace(quarter_directive, str_quarter)
    return str_datetime
