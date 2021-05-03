from django.db import transaction

from statistic.models import AbstractProductStatistic


def import_production_statistic_from_csv(csv_reader):
    production_statistics = []
    for index, row in enumerate(csv_reader):
        if row[0] != 'id':
            current_production_statistic = {
                'ph_product_title': row[1],
                'ffm_product_title': row[2],
                'production_time_default': row[3],
                'est_production_time_default': row[4],
                'shipping_time_default': row[5],
                'est_shipping_time_default': row[6],
                'sort_index': row[7]
            }
            production_statistics.append(current_production_statistic)
    with transaction.atomic():
        AbstractProductStatistic.truncate()
        for production_statistic in production_statistics:
            AbstractProductStatistic(**production_statistic).save()
