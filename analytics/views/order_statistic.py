import pytz
from dateutil.relativedelta import relativedelta
from rest_framework.response import Response

from analytics.function.extend_missing_time_points import extend_missing_time_points
from analytics.function.extract_statistic import extract_statistic_from_objs
from analytics.function.get_time_unit_from_bounded_time import get_time_unit_from_bounded_time
from helper.datetime_helpers import get_start_of_current_day_datetime
from order.filters import CreatedTimeOrderFilter

empty_order_statistics = {"count": {"total": 0,
                                    "fulfill_status": {"unfulfilled": 0, "fulfilled": 0, "in_production": 0,
                                                       "canceled": 0, "rejected": 0, "requested":0},
                                    "financial_status": {"paid": 0, "unpaid": 0, "cancelled": 0, "failed": 0}},
                          "est_profit": {"amount": 0}}


class OrderStatisticView:
    @staticmethod
    def response_order_statistic(request, queryset=None):
        user = request.user
        request_params = request.query_params
        try:
            local_timezone = pytz.timezone(request_params.get("timezone"))
        except Exception as e:
            return Response({"errors": ["Invalid timezone was given"]})

        order_filter = CreatedTimeOrderFilter(request_params, queryset=queryset)
        if not order_filter.is_valid():
            return Response({"errors": order_filter.errors})
        bounded_datetime_order_queryset = order_filter.qs
        field_filters = order_filter.form.cleaned_data
        current_datetime = get_start_of_current_day_datetime()
        until = field_filters.get("until") or current_datetime
        since = field_filters.get("since") or user.create_time
        statistic_unit, extract_time_func, one_unit_time_delta, time_format = get_time_unit_from_bounded_time(since,
                                                                                                              until)

        all_time_order_statistics = bounded_datetime_order_queryset.values(
            "shop__owner_id").order_by().with_statistics()
        by_unit_order_statistics = bounded_datetime_order_queryset.annotate(
            time___at=extract_time_func('create_time', tzinfo=local_timezone)).values(
            'time___at').order_by("-time___at").with_statistics()

        all_time_order_statistics = extract_statistic_from_objs(all_time_order_statistics[:1])
        by_unit_order_statistic_result = extract_statistic_from_objs(by_unit_order_statistics)
        by_unit_order_statistic_full_result = extend_missing_time_points(by_unit_order_statistic_result,
                                                                         time_format,
                                                                         (since, until,
                                                                          one_unit_time_delta), empty_order_statistics)

        return Response(
            {"statistics": {
                "order": {"unit": statistic_unit,
                          "start_datetime": since,
                          "end_datetime": until,
                          "all": all_time_order_statistics[0] if all_time_order_statistics else empty_order_statistics,
                          "scopes": by_unit_order_statistic_full_result}}})
