import json

from xlsxwriter.workbook import Workbook

from abstract_product.constants import ABSTRACT_TYPE_DICT
from abstract_product.models import CategoryProduct, AbstractProductMeta, AbstractProductSide, \
    AbstractProductMockupInfo, ProductAttribute, ProductAttributeValue, AbstractProductVariantAttribute, \
    AbstractProductVariant
from shipping.models import ShippingCostAbstractVariant, ShippingZone


class UserProductService:
    row = 0
    col = 0

    def __init__(self):
        self.worksheet = None
        self.workbook = None

    def write_product_as_xlsx_row(self, abstract_product):
        self.write_brief_info(abstract_product)
        self.write_meta(abstract_product)
        self.write_product_sides(abstract_product)
        self.write_mockups_info(abstract_product)
        self.write_product_attributes(abstract_product)
        self.write_product_attribute_values(abstract_product)
        self.write_shipping_info(abstract_product)
        self.write_product_variant(abstract_product)

    def write_brief_info(self, abstract_product):
        self.write_cell('0')
        self.write_cell(abstract_product.title)
        self.write_cell(abstract_product.sku)
        self.write_cell(abstract_product.sort_index)
        self.write_cell(abstract_product.preview_image_url)

        categories = CategoryProduct.objects.filter(product=abstract_product)
        category_names = ','.join(category.category.title for category in categories if category.category is not None)
        self.write_cell(category_names)
        self.write_cell('visible' if abstract_product.is_catalog_visible else 'hidden')
        self.write_cell(abstract_product.active_mockup_version)
        self.write_cell(ABSTRACT_TYPE_DICT[abstract_product.type])
        self.new_row()

    def write_meta(self, abstract_product):
        self.write_cell('1')
        product_meta = AbstractProductMeta.objects.filter(abstract_product=abstract_product).first()

        self.write_cell(product_meta.description)
        self.write_cell(product_meta.short_description)
        self.ignore_cell()
        self.write_cell(product_meta.pricing_meta)
        self.write_cell(product_meta.template_meta)
        self.write_cell(product_meta.fusion_meta)
        self.write_cell(product_meta.design_note)
        self.new_row()

    def write_product_sides(self, abstract_product):
        sides = AbstractProductSide.objects.filter(abstract_product=abstract_product)
        for side in sides:
            self.write_cell('2')
            self.write_cell(side.type)
            self.write_cell(side.constraints)
            self.write_cell(side.fusion_size)
            self.write_cell('enable_background_color' if side.enable_background_color else '')
            self.new_row()

    def write_mockups_info(self, abstract_product):
        mockup_infos = AbstractProductMockupInfo.objects.filter(abstract_product=abstract_product)
        for mockup_info in mockup_infos:
            self.write_cell('3')
            self.write_cell(mockup_info.name)
            self.write_cell(mockup_info.meta)
            self.write_cell(mockup_info.preview)
            self.write_cell(mockup_info.preview_meta)

            self.new_row()

    def write_product_attributes(self, abstract_product):
        attrs = ProductAttribute.objects.filter(product=abstract_product)
        for attr in attrs:
            self.write_cell('4')
            self.write_cell(attr.name)
            self.write_cell(attr.type)

            self.new_row()

    def write_product_attribute_values(self, abstract_product):
        attrs = ProductAttribute.objects.filter(product=abstract_product)
        for attr in attrs:
            attr_values = ProductAttributeValue.objects.filter(attribute=attr).order_by('sort_index')
            for attr_value in attr_values:
                self.write_cell('5')
                self.write_cell(attr_value.label)
                self.write_cell(attr_value.attribute.type)
                self.write_cell(attr_value.value)

                self.new_row()

    def write_shipping_info(self, abstract_product):
        product_meta = AbstractProductMeta.objects.filter(abstract_product=abstract_product).first()
        shipping_info = product_meta.shipping_meta
        # ignore old format shipping_info['shipping_zones']
        if "shipping_time" not in shipping_info:
            shipping_zones = sorted(shipping_info['shipping_zones'], key=lambda k: ''.join(k['zones']))
            for shipping_zone in shipping_zones:
                self.write_cell('7')
                self.write_cell(', '.join(shipping_zone['zones']))
                self.write_cell(', '.join(shipping_zone['rates']))
                self.write_cell(shipping_zone['delivery_info'])

                self.new_row()

    def write_product_variant(self, abstract_product):
        product_meta = AbstractProductMeta.objects.filter(abstract_product=abstract_product).first()
        shipping_info = product_meta.shipping_meta
        # ignore old format
        if 'processing_time' in shipping_info:
            self.write_cell('old format')
            return

        zone_names = [', '.join(shipping_zone['zones']) for shipping_zone in shipping_info['shipping_zones']]
        zone_names.sort()

        abstract_variants = AbstractProductVariant.objects.filter(product=abstract_product)

        attribute_number = ProductAttribute.objects.filter(product=abstract_product).count()
        self.col = 3 + attribute_number + 1
        for zone_name in zone_names:
            self.worksheet.merge_range(self.row, self.col, self.row, self.col + 3, zone_name)
            self.row += 1
            self.write_cell('Pro Base')
            self.write_cell('Pro Add')
            self.write_cell('Ship Base')
            self.write_cell('Ship Add')
            self.row -= 1
        self.new_row(number=2)
        for abstract_variant in abstract_variants:
            self.write_cell('9')
            self.write_cell(abstract_variant.sku)
            self.write_cell(abstract_variant.title)

            attrs = AbstractProductVariantAttribute.objects.filter(variant=abstract_variant) \
                .order_by('attribute_value__sort_index')
            for attr in attrs:
                if attr.attribute_value is not None:
                    self.write_cell(attr.attribute_value.value)

            self.write_cell(abstract_variant.mockup_info.name)
            shipping_cost_collections = ShippingCostAbstractVariant.objects.filter(
                abstract_variant_sku=abstract_variant.sku)
            for zone_name in zone_names:
                zone = ShippingZone.objects.filter(name=zone_name).first()
                shipping_cost = shipping_cost_collections.filter(shipping_zone=zone).first()
                if shipping_cost is None:
                    continue
                self.write_cell(shipping_cost.production_cost_base)
                self.write_cell(shipping_cost.production_cost_additional)
                self.write_cell(shipping_cost.shipping_cost_base)
                self.write_cell(shipping_cost.shipping_cost_additional)
            self.new_row()

    def write_cell(self, content):
        if type(content) is dict:
            content = json.dumps(content)
        self.worksheet.write(self.row, self.col, content)
        self.col += 1

    def new_row(self, number=1):
        self.row += number
        self.col = 0

    def ignore_cell(self):
        self.col += 1

    def get_xlsx(self, queryset, response):
        self.workbook = Workbook(response, {'in_memory': True})
        self.worksheet = self.workbook.add_worksheet()
        self.new_row()
        for product in queryset:
            self.write_product_as_xlsx_row(product)
            self.new_row()
        self.workbook.close()
