from collections import defaultdict


def extract_statistic_from_objs(statistic_objs):
    statistic_result = []
    for s in statistic_objs:
        statistic_result.append(extract_statistic_from_obj(s))
    return statistic_result


def extract_statistic_from_obj(statistic_obj):
    current_statistic = defaultdict(lambda: defaultdict(dict))
    for k, v in statistic_obj.items():
        attributes = k.split("___")
        attribute_count = len(attributes)
        if attribute_count == 2:
            statistic_type, statistic_name = attributes
            current_statistic[statistic_type][statistic_name] = v
        elif attribute_count == 3:
            statistic_type, statistic_name, sub_statistic_name = attributes
            current_statistic[statistic_type][statistic_name][sub_statistic_name] = v
    return current_statistic
