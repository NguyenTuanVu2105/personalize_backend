from HUB.services.xlsx_supporter.fields import AttributeField
from HUB.services.xlsx_supporter.model_workbook import ModelWorkbook
from HUB.services.xlsx_supporter.model_worksheet import ModelWorksheet


class ShopWorksheet(ModelWorksheet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    id = AttributeField('id', title='id')
    name = AttributeField('name', title='name')
    owner = AttributeField('owner__email', title='owner')
    url = AttributeField('url', title='url')
    status = AttributeField('verbose_status', title='status')

    class Meta:
        name = 'shops'
        fields = ['id', 'name', 'owner', 'status', 'url']


class ShopWorkbook(ModelWorkbook):
    cell_format = {'text_wrap': True, 'valign': 'top'}
    heading_format = {
        'text_wrap': True,
        'valign': 'top',
        'bg_color': '#deebff',
        'bold': True
    }

    def __init__(self, queryset):
        super(ShopWorkbook, self).__init__('orders')
        self.append_worksheet(
            ShopWorksheet(queryset, cell_format=self.cell_format, heading_format=self.heading_format))
