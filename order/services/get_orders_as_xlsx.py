from HUB.services.xlsx_supporter.fields import AttributeField, SerializerField, DatetimeField, MethodField
from HUB.services.xlsx_supporter.model_workbook import ModelWorkbook
from HUB.services.xlsx_supporter.model_worksheet import ModelWorksheet
from order.serializers.order_comments import BriefOrderCommentsSerializer


def get_receiver(order):
    return order.shipping_address.full_name


class OrderWorksheet(ModelWorksheet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    id = AttributeField('id', title='id', column_width=17)
    created_time = DatetimeField('create_time', title='create time')
    owner = AttributeField(source='shop__owner__email', title='owner')
    fulfill_status = AttributeField('verbose_fulfill_status', title='fulfill status', plain_text=True)
    financial_status = AttributeField('verbose_financial_status', title='financial status', plain_text=True)
    total_production_cost = AttributeField('production_cost', title='total production cost')
    shipping_cost = AttributeField('shipping_cost', title='shipping cost')
    total_ph_cost = AttributeField('total_cost', title='total PH cost')
    total_ffm_cost = AttributeField('total_mfr_cost', title='total FFM cost')
    total_price = AttributeField('total_price_in_usd', title='total price')
    receiver = MethodField(method=get_receiver, title='Receiver\'s name')
    receiver_phone = AttributeField('shipping_address__phone', title='Receiver\'s phone')
    address1 = AttributeField('shipping_address__address1', title='Address 1')
    address2 = AttributeField('shipping_address__address2', title='Address 2')
    shipping_city = AttributeField('shipping_address__city', title='Shipping city')
    shipping_province = AttributeField('shipping_address__province', title='Shipping province')
    shipping_country = AttributeField('shipping_address__country', title='Shipping country')
    comments = SerializerField(related_key='order_comments', serializer_class=BriefOrderCommentsSerializer,
                               title='comments')

    class Meta:
        name = 'orders'
        fields = ['id', 'owner', 'fulfill_status', 'financial_status', 'total_production_cost', 'shipping_cost',
                  'total_ph_cost', 'total_ffm_cost', 'total_price', 'receiver', 'receiver_phone',
                  'address1', 'address2', 'shipping_city', 'shipping_province', 'shipping_country', 'comments',
                  'created_time']


class OrderWorkbook(ModelWorkbook):
    cell_format = {'text_wrap': True, 'valign': 'top'}
    heading_format = {
        'text_wrap': True,
        'valign': 'top',
        'bg_color': '#deebff',
        'bold': True
    }

    def __init__(self, queryset):
        super(OrderWorkbook, self).__init__('orders')
        self.append_worksheet(
            OrderWorksheet(queryset, cell_format=self.cell_format, heading_format=self.heading_format))
