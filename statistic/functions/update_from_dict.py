from statistic.models import AbstractProductStatistic, ShippingTimeStatistic
from dateutil import parser


def update_production_statistics(dictData):
    production_statistics = dictData['data']
    for production_statistic in production_statistics:
        queryset = AbstractProductStatistic.objects.filter(ffm_product_title=production_statistic['title'])
        if 'productionTime' in production_statistic:
            queryset.update(production_time_default=production_statistic['productionTime'])
        if 'maxTime' in production_statistic:
            queryset.update(est_production_time_default=production_statistic['maxTime'])


def update_shipping_times(dict_data):
    shipping_times = dict_data['data']
    for shipping_time in shipping_times:
        point = parser.parse(shipping_time['point'])
        queryset = ShippingTimeStatistic.objects.filter(point=point)
        if queryset.count() > 0:
            queryset.update(average_time=shipping_time['averageTime'])
        else:
            shipping_time_statistic = ShippingTimeStatistic(point=point, average_time=shipping_time['averageTime'])
            shipping_time_statistic.save()
