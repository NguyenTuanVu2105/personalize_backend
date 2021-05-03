from abstract_product.functions.retrieve_product_pricing import retrieve_pricing_with_attributes


def retrieve_user_product_variant_with_pricing(user_product):
    response = []
    for user_variant in user_product.user_product_variant_set.all():
        variant_data = {
            "user_variant": user_variant.id,
            "user_product": user_variant.user_product_id,
            "extra_cost": str(user_variant.user_product.extra_cost),
            "title": user_variant.product_title,
            "type": user_variant.type,
            "preview": user_variant.get_preview_mockup(),
            "abstract_variant_data": retrieve_pricing_with_attributes(
                user_variant.abstract_variant_id)
        }
        response.append(variant_data)

    return response


def retrieve_user_product_variant(user_product):
    response = []
    for user_variant in user_product.user_product_variant_set.all():
        variant_data = {
            "user_variant": user_variant.id,
            "user_product": None,
            "extra_cost": str(user_variant.user_product.extra_cost),
            "title": user_variant.product_title,
            "preview": user_variant.get_preview_mockup(),
            "abstract_variant": user_variant.abstract_variant_id
        }
        response.append(variant_data)

    return response
