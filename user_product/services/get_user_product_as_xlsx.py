from django.contrib.postgres.aggregates import ArrayAgg

from HUB.services.xlsx_supporter.fields import AttributeField, DatetimeField
from HUB.services.xlsx_supporter.model_workbook import ModelWorkbook
from HUB.services.xlsx_supporter.model_worksheet import ModelWorksheet


class AdminProductWorksheet(ModelWorksheet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    id = AttributeField('id', title='id', column_width=17)
    name = AttributeField('title', title='name')
    owner_name = AttributeField('user__name', title='owner name')
    owner_email = AttributeField('user__email', title='owner email')
    abstract_product_name = AttributeField('abstract_product__title', title='abstract product name')
    created_time = DatetimeField('create_time', title='create time')
    store = AttributeField('shop__name', title='shop', aggregate=ArrayAgg)

    class Meta:
        name = 'products'
        fields = ['id', 'name', 'abstract_product_name', 'owner_name', 'owner_email', 'store', 'created_time']


class AdminProductWorkbook(ModelWorkbook):
    cell_format = {'text_wrap': True, 'valign': 'top'}
    heading_format = {
        'text_wrap': True,
        'valign': 'top',
        'bg_color': '#deebff',
        'bold': True
    }

    def __init__(self, queryset):
        super(AdminProductWorkbook, self).__init__('admin_product')
        self.append_worksheet(
            AdminProductWorksheet(queryset, cell_format=self.cell_format, heading_format=self.heading_format))
