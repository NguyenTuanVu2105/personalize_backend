import json
import logging
import traceback

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction

from HUB.helpers.auth_helper import retrieve_jwt_payload
# from HUB.jwt_response_payload_handler import auth_response_data
from notification.enums.instant_prompt_types import InstantPromptType
from notification.services.instant_prompt import remove_instant_prompt
from service_communication.constants import InstallAppResponseCode, InstallAppResponseMessage
from service_communication.services.adapter_services import AdapterAppCommunicationService
from shop.constants.shop_status import ShopStatus
from shop.models import Ecommerce, Shop, ShopToken
from system_metadata.models import CurrencyExchangeRate
from user.contants import AccountType
from user.functions import create_user_by_email
from user_product.tasks import create_user_variant_prices_task
from user.tasks import update_geolocation_task

logger = logging.getLogger(__name__)
User = get_user_model()


def retrieve_shop_data(e_commerce, shop_url, access_token):
    try:
        shop = Shop(ecommerce=e_commerce, url=shop_url, access_token=access_token)
        init_app_response = AdapterAppCommunicationService.init_app(shop)
        init_data = init_app_response['data']
        return init_data['shop']

    except Exception as e:
        logger.exception(e)
        raise Exception(e)


def save_shop(shop_url, code, user, client_ip):
    try:
        with transaction.atomic():
            user_id = user.id
            response = get_shop_token(shop_url, code)
            e_commerce = Ecommerce.objects.filter(name="Shopify")[0]
            shop_data = retrieve_shop_data(e_commerce=e_commerce, shop_url=shop_url,
                                           access_token=response['access_token'])

            default_shop_data = {
                "access_token": response['access_token'],
                "status": ShopStatus.ACTIVE,
                "confirm_installation_params": {},
                "email": shop_data['email'],
                "ecommerce_shop_id": shop_data['id'],
                "name": standardize_shop_name(shop_url),
                "location_id": shop_data['primary_location_id'],
                "currency": CurrencyExchangeRate.objects.get(currency=shop_data['currency'])
            }

            if user_id:
                logger.info("AUTH REQUEST - HAVE AN USER ID")
                shop = Shop.objects.update_or_create(ecommerce=e_commerce, url=shop_url, owner_id=user_id,
                                                     defaults=default_shop_data)[0]

                # Shop.objects.filter(url=shop_url).exclude(owner_id=user_id).update(status=ShopStatus.INACTIVE)
                handle_after_success_install(user_id, shop, shop_data['currency'])
                response_data = {
                    "message": InstallAppResponseMessage.SUCCESS,
                    "code": InstallAppResponseCode.SUCCESS
                }

            else:
                logger.info("UNAUTH REQUEST - DO NOT HAVE AN USER ID")
                shops_by_ecommerce = Shop.objects.filter(ecommerce_shop_id=shop_data['id']).status_exclude()
                user = User.objects.filter(email=shop_data['email']).first()

                if not shops_by_ecommerce and not user:
                    response_data = handle_not_shop_and_user(shop_data, e_commerce,
                                                             shop_url, default_shop_data, client_ip)

                elif shops_by_ecommerce:
                    response_data = handle_shop_existed(shop_data, shops_by_ecommerce)

                else:
                    response_data = handle_shop_email_existed(shop_data, e_commerce, shop_url, user, default_shop_data)

            return True, response_data

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.info(str(e))
        return False, {
            "message": InstallAppResponseMessage.ERROR_INSTALL,
            "code": InstallAppResponseCode.ERROR_INSTALL
        }


def standardize_shop_name(shop_url):
    return shop_url.replace(".myshopify.com", "")


def handle_after_success_install(user_id, shop, currency):
    Shop.objects.filter(url=shop.url, status=ShopStatus.UNAUTH).delete()
    AdapterAppCommunicationService.post_init_app(shop)
    Shop.objects.filter(url=shop.url).exclude(id=shop.id).update(status=ShopStatus.INACTIVE)
    create_user_variant_prices_task.delay(user_id, currency)
    remove_instant_prompt(user_id, [InstantPromptType.ADD_SHOP])


def handle_not_shop_and_user(shop_data, e_commerce, shop_url, default_shop_data, client_ip):
    # logger.info("CASE 1 - CASE 1 - CASE 1")
    created_user = create_user_by_email(shop_data['email'], AccountType.SHOPIFY,
                                        shop_data['shop_owner'], shop_data['address1'],
                                        shop_data['phone'])
    transaction.on_commit(lambda: update_geolocation_task.delay(user_id=created_user.id, ip_address=client_ip))
    shop, created = Shop.objects.update_or_create(ecommerce=e_commerce, url=shop_url, owner=created_user,
                                                  defaults=default_shop_data)
    # remove_instant_prompt(created_user.id, [InstantPromptType.ADD_SHOP])
    handle_after_success_install(created_user.id, shop, shop_data['currency'])
    return {
        "message": InstallAppResponseMessage.SUCCESS_NEW_ACCOUNT,
        "code": InstallAppResponseCode.SUCCESS_NEW_ACCOUNT,
        "auth_response": retrieve_jwt_payload(created_user)
    }


def handle_shop_existed(shop_data, shops_by_ecommerce):
    # logger.info("CASE 2 - CASE 2- CASE 2")
    active_shop_by_ecommerce = Shop.objects.filter(ecommerce_shop_id=shop_data['id'],
                                                   status=ShopStatus.ACTIVE).first()
    if active_shop_by_ecommerce:
        # logger.info("CASE 2.1 - CASE 2.1 - CASE 2.1")
        handle_after_success_install(active_shop_by_ecommerce.owner_id, active_shop_by_ecommerce, shop_data['currency'])
        return {
            "message": InstallAppResponseMessage.STORE_EXISTED,
            "code": InstallAppResponseCode.STORE_EXISTED,
            "owner_email": active_shop_by_ecommerce.owner.email
        }
    else:
        # logger.info("CASE 2.2 - CASE 2.2 - CASE 2.2")
        return {
            "message": InstallAppResponseMessage.ALL_STORE_INACTIVE,
            "code": InstallAppResponseCode.ALL_STORE_INACTIVE,
            "owners": [{"email": store.owner.email, "name": store.owner.name, "avatar_url": store.owner.avatar,
                        "active": store.status == ShopStatus.ACTIVE} for store in shops_by_ecommerce]
        }


def handle_shop_email_existed(shop_data, e_commerce, shop_url, user, default_shop_data):
    # logger.info("CASE 3 - CASE 3 - CASE 3")
    shop, created = Shop.objects.update_or_create(ecommerce=e_commerce, url=shop_url, owner=user,
                                                  defaults=default_shop_data)
    handle_after_success_install(user.id, shop, shop_data['currency'])
    return {
        "message": InstallAppResponseMessage.STORE_EMAIL_EXISTED,
        "code": InstallAppResponseCode.STORE_EMAIL_EXISTED,
        "owner_email": user.email
    }


def get_shop_token(shop, code):
    shop_token = ShopToken.objects.filter(code=code).first()
    if shop_token:
        return shop_token.shopify_response

    else:
        url = f'https://{shop}/admin/oauth/access_token'
        data = {
            "code": code,
            "client_id": settings.SHOPIFY_API_KEY,
            "client_secret": settings.SHOPIFY_API_SECRET_KEY
        }
        re = requests.post(url=url, data=data)
        shopify_response = json.loads(re.text)
        # logger.info("RESPONSE: {}".format(re.text))
        ShopToken.objects.update_or_create(code=code, defaults={"shop_url": shop, "shopify_response": shopify_response})
        return shopify_response
