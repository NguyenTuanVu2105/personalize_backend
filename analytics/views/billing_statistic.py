import logging

import pytz
from dateutil.relativedelta import relativedelta
from rest_framework.response import Response

from analytics.function.extend_missing_time_points import extend_missing_time_points
from analytics.function.extract_statistic import extract_statistic_from_obj, extract_statistic_from_objs
from analytics.function.get_time_unit_from_bounded_time import get_time_unit_from_bounded_time
from billing.filters.transaction_filters import CreatedTimeTransactionFilter
from billing.sub_apps.combine_payment.constants import PaymentGateway
from helper.datetime_helpers import get_start_of_current_day_datetime

logger = logging.getLogger(__name__)

empty_billing_statistics = {
    "total": {
        "count": 0, "charge": 0.0, "refund": 0.0, "profit": 0.0
    },
    "braintree": {
        "count": 0, "charge": 0.0, "refund": 0.0, "profit": 0.0
    },
    "stripe": {
        "count": 0, "charge": 0.0, "refund": 0.0, "profit": 0.0
    },
    "payoneer": {
        "count": 0, "charge": 0.0, "refund": 0.0, "profit": 0.0
    }
}


class BillingStatisticView:
    @staticmethod
    def response_billing_statistic(request, queryset=None):
        request_params = request.query_params
        try:
            local_timezone = pytz.timezone(request_params.get("timezone"))
        except Exception as e:
            return Response({"errors": ["Invalid timezone was given"]})

        billing_filter = CreatedTimeTransactionFilter(request_params, queryset=queryset)
        if not billing_filter.is_valid():
            return Response({"errors": billing_filter.errors})
        bounded_datetime_billing_queryset = billing_filter.qs
        field_filters = billing_filter.form.cleaned_data
        current_datetime = get_start_of_current_day_datetime()
        until = field_filters.get("until") or current_datetime
        since = field_filters.get("since") or current_datetime - relativedelta(years=2)
        statistic_unit, extract_time_func, one_unit_time_delta, time_format = get_time_unit_from_bounded_time(since,
                                                                                                              until)
        # all time
        list_payment_statics = [PaymentGateway.PAYPAL_PRO, PaymentGateway.PAYONEER, PaymentGateway.PAYPAL_VAULT]
        all_time_billing = extract_statistic_from_obj(
            bounded_datetime_billing_queryset.with_statistics(annotate=False,
                                                              list_payment_gateway=list_payment_statics))

        # scope
        by_unit_billing = bounded_datetime_billing_queryset.annotate(
            time___at=extract_time_func('create_time', tzinfo=local_timezone)).values('time___at').order_by(
            'time___at').with_statistics()
        by_unit_billing_result = extract_statistic_from_objs(by_unit_billing)
        by_unit_billing_result = extend_missing_time_points(by_unit_billing_result,
                                                            time_format,
                                                            (since, until,
                                                             one_unit_time_delta), empty_billing_statistics)
        return Response(
            {"statistics": {
                "billing": {"unit": statistic_unit,
                            "start_datetime": since,
                            "end_datetime": until,
                            "all": all_time_billing if all_time_billing else empty_billing_statistics,
                            "scopes": by_unit_billing_result}}})
