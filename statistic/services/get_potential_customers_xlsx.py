import json

from django.contrib.postgres.aggregates import ArrayAgg
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q, Count

from HUB.services.xlsx_supporter.fields import AttributeField, MethodField, DatetimeField
from HUB.services.xlsx_supporter.model_workbook import ModelWorkbook
from HUB.services.xlsx_supporter.model_worksheet import ModelWorksheet
from billing.sub_apps.combine_payment.models import GeneralPaymentMethod
from order.constants.financial_statuses import OrderFinancialStatus


def get_existed_time_without_product(instance):
    if instance.product_set is not None and instance.product_set.count() > 0:
        return 'created product'
    return instance.existed_time.days


def get_existed_time_without_payment(instance):
    if instance.is_valid_payment:
        all_payments = GeneralPaymentMethod.objects.active().by_user(instance.id)
        return 'added {} payment'.format(all_payments.count())
    else:
        return instance.existed_time.days


def get_payments(instance):
    if instance.is_valid_payment:
        all_payments = GeneralPaymentMethod.objects.active().by_user(instance.id)
        return ',\n'.join([json.dumps(payment.payment_gateway_method_data,
                                      cls=DjangoJSONEncoder)
                           for payment in all_payments
                           if payment])
    else:
        return ''


class PotentialCustomersOverviewWorksheet(ModelWorksheet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    id = AttributeField('id', title='id', column_width=15)
    name = AttributeField('name', title='name', column_width=24)
    email = AttributeField('email', title='email', column_width=32)
    phone = AttributeField('phone_number', title='phone number', column_width=17)
    create_time = DatetimeField('create_time', title='create time', column_width=32)
    existed_time_without_product = MethodField(method=get_existed_time_without_product,
                                               title='existed time without product',
                                               column_width=20)
    existed_time_without_payment = MethodField(method=get_existed_time_without_payment,
                                               title='existed time without payment',
                                               column_width=20)
    country_code = AttributeField('country_code', title='Country code')
    payments = MethodField(method=get_payments, title='payments', column_width=32)
    all_shop = AttributeField('shop__url',
                              aggregate=ArrayAgg,
                              agg_filter=Q(shop__url__isnull=False) & ~Q(shop__url=''),
                              agg_distinct=True, title='all shop', column_width=26)
    created_product = AttributeField('product_set__abstract_product__title',
                                     aggregate=ArrayAgg,
                                     agg_distinct=True, title='Created products')
    num_charged_order = AttributeField('shop__orders',
                                       agg_filter=Q(shop__orders__financial_status=OrderFinancialStatus.PAID),
                                       aggregate=Count, agg_distinct=True, title='Num charged orders')
    synced_shop = AttributeField('product_set__shop_user_product_set__shop__url',
                                 aggregate=ArrayAgg,
                                 agg_filter=Q(product_set__shop_user_product_set__shop__url__isnull=False) &
                                            ~Q(product_set__shop_user_product_set__shop__url=''),
                                 agg_distinct=True,
                                 title='synced shop', column_width=26)

    class Meta:
        name = 'overview'
        fields = ['id', 'name', 'email', 'phone', 'country_code', 'existed_time_without_product',
                  'existed_time_without_payment', 'num_charged_order',
                  'payments', 'created_product', 'all_shop', 'synced_shop', 'create_time']


class CustomerWithoutProductWorksheet(ModelWorksheet):
    id = AttributeField('id', title='id', column_width=15)
    name = AttributeField('name', title='name', column_width=24)
    email = AttributeField('email', title='email', column_width=32)
    country_code = AttributeField('country_code', title='Country code')
    create_time = DatetimeField('create_time', title='create time', column_width=32)
    existed_time = MethodField(method=lambda instance: instance.existed_time.days,
                               title='existed time')

    class Meta:
        name = 'Customer with no product'
        fields = ['id', 'name', 'email', 'country_code', 'create_time', 'existed_time']


class CustomerWithoutPaymentWorksheet(ModelWorksheet):
    id = AttributeField('id', title='id', column_width=15)
    name = AttributeField('name', title='name', column_width=24)
    email = AttributeField('email', title='email', column_width=32)
    country_code = AttributeField('country_code', title='Country code')
    create_time = DatetimeField('create_time', title='create time', column_width=32)

    class Meta:
        name = 'Customer with no payment'
        fields = ['id', 'name', 'email', 'country_code', 'create_time']


class CustomerWithLinkedShopWorksheet(ModelWorksheet):
    id = AttributeField('id', title='id', column_width=15)
    name = AttributeField('name', title='name', column_width=24)
    email = AttributeField('email', title='email', column_width=32)
    country_code = AttributeField('country_code', title='Country code')
    create_time = DatetimeField('create_time', title='create time', column_width=32)

    class Meta:
        name = 'Customer with linked shop'
        fields = ['id', 'name', 'email', 'country_code', 'create_time']


class PotentialCustomersWorkbook(ModelWorkbook):
    cell_format = {'text_wrap': True, 'valign': 'top'}
    heading_format = {
        'text_wrap': True,
        'valign': 'top',
        'bg_color': '#deebff',
        'bold': True
    }

    def __init__(self, queryset):
        super(PotentialCustomersWorkbook, self).__init__('potential_customers')
        self.append_worksheet(PotentialCustomersOverviewWorksheet(queryset,
                                                                  cell_format=self.cell_format,
                                                                  heading_format=self.heading_format))
        user_without_product = queryset.filter(product_set__isnull=True, )
        self.append_worksheet(CustomerWithoutProductWorksheet(user_without_product,
                                                              cell_format=self.cell_format,
                                                              heading_format=self.heading_format))
        user_without_payment = queryset.filter(is_valid_payment=False)
        self.append_worksheet(CustomerWithoutPaymentWorksheet(user_without_payment,
                                                              cell_format=self.cell_format,
                                                              heading_format=self.heading_format))
        user_with_linked_shop = queryset.filter(product_set__shop_user_product_set__isnull=False).distinct()
        self.append_worksheet(CustomerWithLinkedShopWorksheet(user_with_linked_shop,
                                                              cell_format=self.cell_format,
                                                              heading_format=self.heading_format))
