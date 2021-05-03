from helper.datetime_helpers import str_from_datetime

import logging
logger = logging.getLogger(__name__)

def extend_missing_time_points(by_day_statistic_result, time_format, time_info, empty_statistics):
    since, until, one_unit_time_delta = time_info
    by_day_statistic_result_dict = {str_from_datetime(result["time"]["at"], time_format): result for result in
                                    by_day_statistic_result}
    by_day_statistic_full_result = []
    loop_current_datetime = since
    while True:
        current_day = str_from_datetime(loop_current_datetime, time_format)
        if current_day > str_from_datetime(until, time_format):
            break
        current_day_statistic = by_day_statistic_result_dict.get(current_day)
        if not current_day_statistic:
            current_day_statistic = {"time": {"at": current_day}, **empty_statistics}
        else:
            current_day_statistic["time"]["at"] = current_day

        by_day_statistic_full_result.append(current_day_statistic)
        loop_current_datetime += one_unit_time_delta
    return by_day_statistic_full_result
