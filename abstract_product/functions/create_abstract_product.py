import logging

from abstract_product.models import AbstractProductCategory, AbstractProduct, AbstractProductMeta, \
    AbstractProductVariant, AbstractProductSide, AbstractProductMockupInfo, ProductAttribute, ProductAttributeValue, \
    AbstractProductVariantAttribute, CategoryProduct
from shipping.models import ShippingRate, ShippingZone, ShippingCostAbstractVariant

logger = logging.getLogger(__name__)

ADD_TO_TRENDING = True
DELETE_OLD_CATEGORIES = True
BASE_COST = 6.5
SELECT_TYPE = "choice"
STANDARD_SIZE = {
    "height": 1000,
    "width": 1000
}

CATEGORIES = [
    "Trending",
    "Classic Apparel",
    "Home & Living"
]


def create_categories():
    for index, category_name in enumerate(CATEGORIES):
        print("Creating abstract categories: {} ...".format(category_name))
        category_queryset = AbstractProductCategory.objects.filter(title=category_name, is_active=True)
        if len(category_queryset) == 0:
            AbstractProductCategory.objects.create(title=category_name, is_active=True, sort_index=index + 1)


category_index = 0


def create_abstract_product_from_dict_data(abstract_product_data, last_order_dict, max_existed_order, deactivate=True,
                                           update=True):
    try:
        print("Creating abstract product: {} ...".format(abstract_product_data['title']))
        print("Creating abstract product: {} ...".format(abstract_product_data['type']))
        product_sku = abstract_product_data['sku']
        sort_index = last_order_dict[product_sku] if product_sku in last_order_dict else max_existed_order + 1
        if update:
            abstract_product, created = AbstractProduct.objects \
                .update_or_create(sku=product_sku,
                                  is_active=True,
                                  defaults={
                                      'title': abstract_product_data['title'],
                                      'preview_image_url': abstract_product_data['preview'],
                                      'sort_index': sort_index,
                                      'is_catalog_visible': abstract_product_data['is_catalog_visible'],
                                      'active_mockup_version': abstract_product_data['active_mockup_version'],
                                      'type': abstract_product_data['type']
                                  })
        else:
            abstract_product = AbstractProduct.objects \
                .create(title=abstract_product_data['title'],
                        is_active=True,
                        preview_image_url=abstract_product_data['preview'],
                        sku=product_sku,
                        is_catalog_visible=abstract_product_data['is_catalog_visible'],
                        sort_index=sort_index,
                        active_mockup_version=abstract_product_data['active_mockup_version'],
                        type=abstract_product_data['type'])

        print(abstract_product)
        abstract_product_data['shipping_meta']['shipping_zones'] = abstract_product_data["shipping_info"]
        AbstractProductMeta.objects \
            .update_or_create(abstract_product=abstract_product,
                              defaults={
                                  "description": abstract_product_data['description'],
                                  "short_description": abstract_product_data['short_description'],
                                  "base_cost": abstract_product_data['base_cost'],
                                  "shipping_meta": abstract_product_data['shipping_meta'],
                                  "pricing_meta": abstract_product_data['pricing_meta'],
                                  "template_meta": abstract_product_data['template_meta'],
                                  "fusion_meta": abstract_product_data['fusion_meta'],
                                  "design_note": abstract_product_data['design_note']
                              })
        for side_data in abstract_product_data["sides"]:
            AbstractProductSide.objects \
                .update_or_create(abstract_product=abstract_product,
                                  type=side_data["name"],
                                  defaults={
                                      "constraints": side_data["constraints"],
                                      "fusion_size": side_data["fusion_size"],
                                      "enable_background_color": side_data["enable_background_color"]
                                  }
                                  )
        mockups = {}
        AbstractProductMockupInfo.objects.filter(abstract_product=abstract_product).delete()
        for mockup_name, mockup_data in abstract_product_data["mockups"].items():
            mockup, created = AbstractProductMockupInfo.objects. \
                update_or_create(abstract_product=abstract_product,
                                 name=mockup_name,
                                 defaults={
                                     "meta": mockup_data["meta"],
                                     "preview": mockup_data["preview"],
                                     "preview_meta": mockup_data["preview_meta"],
                                     # "enable_preview": mockup_data["enable_preview"],
                                 })
            mockups[mockup_name] = mockup
        ProductAttribute.objects.filter(product=abstract_product).update(is_active=False)
        attributes = {}
        for attribute_type, attribute_data in abstract_product_data["attributes"].items():
            attribute, created = ProductAttribute.objects \
                .update_or_create(product=abstract_product,
                                  type=attribute_type,
                                  defaults={
                                      "is_active": True,
                                      "name": attribute_data["name"],
                                      "sort_index": attribute_data["sort_index"]
                                  }
                                  )
            attributes[attribute_type] = attribute
        attribute_values = {}
        ProductAttributeValue.objects.filter(attribute__product=abstract_product).update(is_active=False)
        for sort_index, attribute_value_data in enumerate(abstract_product_data["attribute_values"]):
            attribute_value, created = ProductAttributeValue.objects \
                .update_or_create(attribute=attributes[attribute_value_data["type"]],
                                  value=attribute_value_data["value"],
                                  defaults={
                                      "label": attribute_value_data["label"],
                                      "sort_index": sort_index,
                                      "is_active": True
                                  })
            attribute_values[attribute_value_data["value"]] = attribute_value
        shipping_rates = {}
        shipping_zones = {}
        shipping_info = abstract_product_data["shipping_info"]
        for shipping in shipping_info:
            for shipping_zone_code in shipping["zones"]:
                shipping_zones[shipping_zone_code] = ShippingZone.objects.filter(name=shipping_zone_code).first()
            for shipping_rate_code in shipping["rates"]:
                shipping_rates[shipping_rate_code] = ShippingRate.objects.filter(slug=shipping_rate_code).first()

        AbstractProductVariant.objects.filter(product=abstract_product, user_product_variant_set=None).delete()
        AbstractProductVariant.objects.filter(product=abstract_product).update(is_active=False)
        for variant in abstract_product_data["variants"]:
            abstract_variant, created = AbstractProductVariant.objects \
                .update_or_create(product=abstract_product,
                                  sku=variant["sku"],
                                  defaults={
                                      "title": variant['title'],
                                      "mockup_info": mockups[variant['mockup']] if variant['mockup'] != '' else None,
                                      "is_active": True
                                  })
            AbstractProductVariantAttribute.objects.filter(variant=abstract_variant).delete()
            for attribute_value in variant["attributes"]:
                AbstractProductVariantAttribute.objects.create(variant=abstract_variant,
                                                               attribute_value=attribute_values[attribute_value])

            for shipping_price in variant["shipping_prices"]:
                ShippingCostAbstractVariant.objects.update_or_create(abstract_variant_sku=abstract_variant.sku,
                                                                     shipping_rate=shipping_rates[
                                                                         shipping_price["shipping_rate"]],
                                                                     shipping_zone=shipping_zones[
                                                                         shipping_price["shipping_zone"]],
                                                                     defaults={
                                                                         "production_cost_base": shipping_price[
                                                                             "production_cost_base"],
                                                                         "production_cost_additional": shipping_price[
                                                                             "production_cost_additional"],
                                                                         "shipping_cost_base": shipping_price[
                                                                             "shipping_cost_base"],
                                                                         "shipping_cost_additional": shipping_price[
                                                                             "shipping_cost_additional"]
                                                                     })
        if deactivate:
            AbstractProductCategory.objects.filter(is_active=False).delete()
        for category_name in abstract_product_data['categories']:
            category, created = AbstractProductCategory.objects \
                .get_or_create(title=category_name,
                               defaults={
                                   "preview_image_url": abstract_product_data["preview"],
                                   "is_active": True,
                                   "sort_index": abstract_product_data['sort_index']
                               })
            CategoryProduct.objects.update_or_create(product=abstract_product, category=category)
        return abstract_product
    except Exception as e:
        logger.exception(e)
