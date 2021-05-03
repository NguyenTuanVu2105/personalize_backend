from HUB.services.xlsx_supporter.fields import AttributeField
from HUB.services.xlsx_supporter.model_workbook import ModelWorkbook
from HUB.services.xlsx_supporter.model_worksheet import ModelWorksheet


class SuppliedProductMappingWorksheet(ModelWorksheet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    supplier = AttributeField('verbose_supplier', title='Supplier')
    ph_product_sku = AttributeField('ph_product_sku', title='Printholo sku')
    supplier_product_sku = AttributeField('supplier_product_sku', title='Supplier sku')

    class Meta:
        name = 'Sku mapping'
        fields = ['supplier', 'ph_product_sku', 'supplier_product_sku']


class SuppliedProductMappingWorkbook(ModelWorkbook):

    cell_format = {'text_wrap': True, 'valign': 'top'}
    heading_format = {
        'text_wrap': True,
        'valign': 'top',
        'bg_color': '#deebff',
        'bold': True
    }

    def __init__(self, queryset):
        super(SuppliedProductMappingWorkbook, self).__init__('orders')
        self.append_worksheet(
            SuppliedProductMappingWorksheet(queryset, cell_format=self.cell_format, heading_format=self.heading_format))