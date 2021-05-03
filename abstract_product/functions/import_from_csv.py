import logging
import operator

from django.db import transaction
from kombu.utils import json

from abstract_product.models import AbstractProductCategory, AbstractProduct, CategoryProduct
from .create_abstract_product import create_abstract_product_from_dict_data
from ..constants import ABSTRACT_TYPE_VERBOSE_DICT

logger = logging.getLogger(__name__)


def handle_variant_sku(product_sku, concated_attributes):
    subfix = concated_attributes.replace(" ", "").replace("/", "-")
    subfix = subfix.replace("*", "").replace("x", "")
    subfix = subfix.upper()
    return product_sku + "-" + subfix


def import_from_csv(csv_reader, update=False, deactivate=True):
    products = []
    current_product = {}
    product_index = 0
    for index, row in enumerate(csv_reader):
        # print(row)
        logger.info(row)
        if row[0] == '0':
            product_index += 1
            print("New Product")
            current_product = {
                "sides": [],
                "attributes": {},
                "mockups": {},
                "attribute_values": [],
                "variants": [],
                "shipping_info": []
            }
            products.append(current_product)

            current_product["title"] = row[1]
            current_product["sku"] = row[2]
            current_product["sort_index"] = int(row[3])
            current_product["preview"] = row[4]
            current_product["is_catalog_visible"] = False if row[6] == 'hidden' else True
            current_product["categories"] = list(map(lambda s: s.strip(), row[5].split(",")))
            current_product['active_mockup_version'] = row[7]
            current_product["type"] = ABSTRACT_TYPE_VERBOSE_DICT[row[8]]

        elif row[0] == '1':
            current_product["description"] = row[1]
            current_product["short_description"] = row[2]
            current_product["shipping_meta"] = {}
            current_product["pricing_meta"] = json.loads(row[4])
            current_product["template_meta"] = json.loads(row[5])
            current_product["fusion_meta"] = json.loads(row[6])
            current_product['base_cost'] = 9999999
            current_product['additional_cost'] = 999999
            current_product['design_note'] = row[7]

        elif row[0] == '2':
            extra_info = row[4]
            current_product["sides"].append({
                "name": row[1],
                "constraints": json.loads(row[2]),
                "fusion_size": json.loads(row[3]),
                "enable_background_color": ("enable_background_color" in extra_info)
            })
        elif row[0] == '3':
            current_product["mockups"][row[1]] = {
                "meta": json.loads(row[2]),
                "preview": json.loads(row[3]),
                # "enable_preview": (len(row) > 4 and row[4] == 'enable_preview'),
                "preview_meta": json.loads(row[4])
            }
        elif row[0] == '4':
            current_product["attributes"][row[2]] = {
                "name": row[1],
                "type": row[2],
                "values": [],
                "sort_index": index
            }
        elif row[0] == '5':
            current_product["attribute_values"].append({
                "type": row[2],
                "value": row[3],
                "label": row[1]
            })
        elif row[0] == '7':
            current_product["shipping_info"].append({
                "zones": row[1].strip().split(','),
                "rates": row[2].strip().split(','),
                "delivery_info": json.loads(row[3])
            })

        elif row[0] == '9':

            attributes = []
            attribute_count = len(current_product["attributes"].keys())
            sku = row[1]
            title = row[2]
            i = 2
            # Attribute
            for attribute_index in range(attribute_count):
                i += 1
                attributes.append(row[i])

            # Mockup
            i += 1
            mockup = row[i]

            i += 1
            shipping_prices = []
            logger.info(title)
            logger.info(row)
            logger.info(current_product["shipping_info"])
            for shipping_info in current_product["shipping_info"]:
                for shipping_rate in shipping_info["rates"]:
                    production_cost_base = float(row[i])
                    production_cost_additional = float(row[i + 1])
                    shipping_cost_base = float(row[i + 2])
                    shipping_cost_additional = float(row[i + 3])
                    if current_product['base_cost'] > production_cost_base:
                        current_product['base_cost'] = production_cost_base
                    if current_product['additional_cost'] > production_cost_additional:
                        current_product['additional_cost'] = production_cost_additional
                    for shipping_zone in shipping_info["zones"]:
                        shipping_prices.append({
                            "shipping_zone": shipping_zone,
                            "shipping_rate": shipping_rate,
                            "production_cost_base": production_cost_base,
                            "production_cost_additional": production_cost_additional,
                            "shipping_cost_base": shipping_cost_base,
                            "shipping_cost_additional": shipping_cost_additional
                        })
                    i += 4

            current_product["variants"].append({
                "title": title,
                "sku": sku,
                "attributes": attributes,
                "mockup": mockup,
                "shipping_prices": shipping_prices
            })

    print("DONE READ CSV")

    if not deactivate and AbstractProduct.objects.filter(sku__in=list(map(lambda prod: prod['sku'], products))) \
            .filter(is_active=True).count() > 0:
        raise ValueError('Cannot import: sku {} is active'.format(current_product['sku']))
    with transaction.atomic():
        last_order_dict, max_existed_order = retrieve_last_product_order()
        if deactivate:
            AbstractProductCategory.objects.all().delete()
        abstract_product_ids = []
        category_all, created = AbstractProductCategory.objects.get_or_create(title="All Products",
                                                                              defaults={'preview_image_url': "",
                                                                                        'is_active': True,
                                                                                        'sort_index': -1})
        for product in products:
            print(json.dumps(product))
            abstract_product = create_abstract_product_from_dict_data(product, last_order_dict, max_existed_order,
                                                                      deactivate, update)
            abstract_product_ids.append(abstract_product.id)
            CategoryProduct.objects.update_or_create(product=abstract_product, category=category_all)
        if deactivate:
            AbstractProduct.objects.all().update(is_active=False)
            AbstractProduct.objects.filter(id__in=abstract_product_ids).update(is_active=True)


def retrieve_last_product_order():
    last_order = AbstractProduct.objects.filter(is_active=True).only('sku', 'sort_index')
    last_order_dict = dict((i.sku, i.sort_index) for i in last_order)
    max_existed_order_key = max(last_order_dict.items(), key=operator.itemgetter(1))[0]
    max_existed_order = last_order_dict[max_existed_order_key]

    return last_order_dict, max_existed_order
