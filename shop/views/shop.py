import logging
import traceback
import urllib

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from HUB.helpers.auth_helper import retrieve_jwt_payload
from HUB.viewsets.base import AuthenticatedGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from service_communication.services.adapter_services import AdapterAppCommunicationService
from shop.constants.shop_status import ShopStatus
from shop.filters import ShopFilter
from shop.forms import VerifyStoreForm, InitStoreForm
from shop.functions import verify_shopify_embedded_request
from shop.models import Shop, Ecommerce
from shop.paginations import ShopPagination
from shop.serializers import ShopSerializer
from shop.serializers.shop import ShopDetailSerializer, BriefShopSerializer
from user.tasks import send_warning_authenication_task
from user_product.models import UserProduct

logger = logging.getLogger(__name__)


class ShopViewSet(SearchableListModelMixin, ListModelMixin,
                  RetrieveModelMixin,
                  AuthenticatedGenericViewSet):
    queryset = Shop.objects.prefetch_related('ecommerce', 'currency').ecommerce_exclude().status_exclude().order_by(
        "-create_time")
    serializer_class = ShopSerializer
    pagination_class = ShopPagination
    filterset_class = ShopFilter
    ordering_fields = ['id', 'owner', 'name', 'currency', 'update_time', 'create_time']

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user.pk)

    @action(methods=["POST"], detail=True, url_path="deactivate")
    def deactivate(self, request, *args, **kwargs):
        shop = self.get_object()
        AdapterAppCommunicationService.uninstall_app(shop)
        shop.status = ShopStatus.INACTIVE
        shop.save()
        return Response({"success": True})

    @action(methods=["GET"], detail=False, url_path="all")
    def get_shop_without_pagination(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return Response(self.serializer_class(queryset, many=True).data)

    @action(methods=["GET"], detail=True, url_path="statistic")
    def statistic(self, request, *args, **kwargs):
        shop = self.get_object()
        user_product_in_shop = UserProduct.objects.filter(user=self.request.user.pk,
                                                          shop_user_product_set__shop_id=shop.id).count()
        total_product = UserProduct.objects.count()
        shop_data = ShopDetailSerializer(instance=shop).data
        shop_data.update({
            "user_product_in_shop": user_product_in_shop,
            "total_user_product": total_product
        })
        return Response(shop_data)

    @action(methods=["POST"], detail=False, url_path="verify", permission_classes=[AllowAny, ])
    def verify_store(self, request, *args, **kwargs):
        request_data = request.data
        verify_store_form = VerifyStoreForm(data=request_data)

        if verify_store_form.is_valid():
            query_params = urllib.parse.parse_qsl(request_data.get("query_string"))
            shop_url = dict(query_params)['shop'] or ''

            shop = Shop.objects.filter(url=shop_url, status=ShopStatus.ACTIVE).first()
            unauth_shop = Shop.objects.filter(url=shop_url, status=ShopStatus.UNAUTH).first()

            # check HMAC SHA-256
            is_embedded_request = verify_shopify_embedded_request(query_params)
            # logger.info("is_embedded_request")
            # logger.info(is_embedded_request)

            if unauth_shop:
                return Response({
                    "success": True,
                    "code": ShopStatus.UNAUTH,
                    "params": unauth_shop.confirm_installation_params
                })

            elif shop and is_embedded_request:
                shop.reset_api_error_count()
                user = shop.owner
                if user.is_lock:
                    return Response({"success": False, "message": "User is disabled"})
                # if not user.is_email_confirmed:
                #     send_warning_authenication_task.delay(user_id=user.id)
                return Response({
                    "success": True,
                    "code": ShopStatus.ACTIVE,
                    "store": BriefShopSerializer(shop).data,
                    "data": retrieve_jwt_payload(shop.owner),
                })

            else:
                return Response({"success": False, "message": "Shop or HMAC-SHA256 is invalid"})

        else:
            errors = [error for error in verify_store_form.errors]
            return Response(data={"success": False, 'message': 'This fields is required:  {}'.format(errors)},
                            status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, url_path="init", permission_classes=[AllowAny, ])
    def init_store(self, request, *args, **kwargs):
        request_data = request.data
        init_store_form = InitStoreForm(data=request_data)

        if init_store_form.is_valid():
            try:
                store = request_data.get("shop")
                e_commerce = Ecommerce.objects.filter(name="Shopify")[0]
                is_embedded_request = verify_shopify_embedded_request([(k, v) for k, v in request_data.items()])
                # logger.info("is_embedded_request")
                # logger.info(is_embedded_request)

                if is_embedded_request:
                    Shop.objects.filter(url=store, status=ShopStatus.UNAUTH).delete()
                    shop = Shop.objects.create(ecommerce=e_commerce, url=store,
                                               status=ShopStatus.UNAUTH,
                                               confirm_installation_params=request_data)

                    return Response({"success": True, "data": "This store has been successfully initialized"})

                else:
                    return Response({"success": False, "message": "Shop or HMAC-SHA256 is invalid"})

            except Exception as e:
                traceback.print_tb(e.__traceback__)
                logger.info(str(e))
                return Response({"success": False, "message": str(e)})

        else:
            errors = [error for error in init_store_form.errors]
            return Response(data={"success": False, 'message': 'This fields is required:  {}'.format(errors)},
                            status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path="default")
    def default(self, request, *args, **kwargs):
        shop_default = Shop.objects.filter(url='', owner_id=self.request.user.pk).first()
        return Response({"id": shop_default.id})
