from collections import OrderedDict


def remove_duplicate(_list):
    return list(OrderedDict.fromkeys(_list))
