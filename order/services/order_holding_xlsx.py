from HUB.services.xlsx_supporter.fields import AttributeField
from HUB.services.xlsx_supporter.model_workbook import ModelWorkbook
from HUB.services.xlsx_supporter.model_worksheet import ModelWorksheet


class OrderHoldingWorkbook(ModelWorkbook):
    cell_format = {'text_wrap': True, 'valign': 'top'}
    heading_format = {
        'text_wrap': True,
        'valign': 'top',
        'bg_color': '#deebff',
        'bold': True
    }

    def __init__(self, queryset):
        super(OrderHoldingWorkbook, self).__init__('orders_holding')
        self.append_worksheet(
            OrderHoldingWorksheet(queryset, cell_format=self.cell_format, heading_format=self.heading_format))


class OrderHoldingWorksheet(ModelWorksheet):
    id = AttributeField('id', title='Id')
    fulfillment_payload = AttributeField('fulfillment_payload', title='Fulfillment payload')
    printholo_cost = AttributeField('printholo_cost', title='printholo cost')
    fulfillment_cost = AttributeField('fulfillment_cost', title='Fullfillment cost')
    order = AttributeField('order__id', title='Order id')

    class Meta:
        name = 'Order holding'
        fields = ['id', 'fulfillment_payload', 'printholo_cost', 'fulfillment_cost', 'order']
