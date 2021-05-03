from django.db import models, connection
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel


class AbstractProductStatistic(RandomIDModel):
    sku = models.CharField(max_length=255, unique=True, verbose_name=_('SKU'), null=True)
    ph_product_title = models.CharField(max_length=255, null=True, verbose_name=_('Title'))
    ffm_product_title = models.CharField(max_length=255, null=True, verbose_name=_('Slug'))
    production_time_default = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    est_production_time_default = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    shipping_time_default = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    est_shipping_time_default = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    sort_index = models.SmallIntegerField(default=0, verbose_name='Sort Index')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'statistic_abstract_product'
        ordering = ['sort_index', 'id']
        verbose_name = _('Abstract Product Statistic')
        verbose_name_plural = _('Abstract Products Statistic')

    def __str__(self):
        return self.ph_product_title

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(cls._meta.db_table))
