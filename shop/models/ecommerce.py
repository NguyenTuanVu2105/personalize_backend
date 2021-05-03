from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel


class Ecommerce(RandomIDModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ecommerce'
        ordering = ['id']
        verbose_name = _('E-Commerce Platform')
        verbose_name_plural = _('E-Commerce Platforms')

    def __str__(self):
        return self.name
