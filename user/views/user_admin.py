import datetime
import traceback

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, FieldError
from django.utils import timezone
from rest_framework import mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response

from HUB.permissions import method_permission_required, get_permissions
from HUB.viewsets.base import AdminGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from user.contants import RATE_LIMIT_VIEW_CHOICES, RATE_LIMIT_PREFIX
from user.filters import UserAdministrationFilter
from user.functions import retrieve_max_allow_rate_limit, get_rate_limit, set_rate_limit, logout_all_device
from user.models import UserLimit
from user.paginations import UserAdministrationPagination
from user.serializers.user import AdminUserSerializer, UserDetailSerializer, BriefUserSerializer
from user.tasks import send_activation_email_task

User = get_user_model()
import logging

logger = logging.getLogger(__name__)


class AdminUserViewSet(SearchableListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       AdminGenericViewSet):
    queryset = User.objects.all()
    filterset_class = UserAdministrationFilter
    pagination_class = UserAdministrationPagination
    serializer_class = AdminUserSerializer

    def get_queryset(self):
        return self.queryset.order_by('-create_time')

    @method_permission_required(get_permissions(['admin_user_view', ]))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_permission_required(get_permissions(['admin_user_view', ]))
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = UserDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    @method_permission_required(get_permissions(['admin_update_user', ]))
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed(request.method)
        updatable = ['is_test_user']
        for field in request.data:
            if field not in updatable:
                return Response({
                    'success': False,
                    'message': '{} is not updatable'.format(field)
                })
        return super().update(request, *args, **kwargs)

    @action(methods=["PUT", 'PATCH', ], detail=False, url_path="bulk_mark_test_user",
            permission_classes=get_permissions(['admin_update_user', ]))
    def bulk_mark_test_user(self, request):
        ids = request.data['ids']
        response_data = []
        for user_id in ids:
            user = self.queryset.get(pk=user_id)
            user.is_test_user = True
            user.save()
            response_data.append({
                'id': user_id,
                'email': user.email,
                'name': user.name,
                'success': True
            })
        return Response({'data': response_data})

    @action(methods=["POST"], detail=False, url_path="change-password",
            permission_classes=get_permissions(['admin_user_change_password', ]))
    def change_password(self, request):
        request_data = request.data
        user_id = request_data['id']
        try:
            user = User.objects.get(id=user_id)
            if 'new_password' in request_data:
                user.set_password(request_data['new_password'])
                now = timezone.now()
                user.last_change_password = now
                user.save()
            else:
                raise ValidationError("Do not Input New Password")
        except User.DoesNotExist:
            return Response({'success': False, 'message': "User not found"})
        except ValidationError:
            return Response({'success': False, 'message': "Do not Input New Password"})
        except Exception as e:
            return Response({'success': False, "message": e})
        else:
            return Response({'success': True, "message": "Change successfully"})

    @action(methods=["GET"], detail=True, url_path="token",
            permission_classes=get_permissions(['admin_user_login_as', ]))
    def get_token(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            token, created = Token.objects.get_or_create(user=user)
        except Exception as e:
            return Response({'success': False, "message": e})
        else:
            return Response({'token': token.key})

    @action(methods=["PUT"], detail=False, url_path="change-rule",
            permission_classes=get_permissions(['admin_user_change_role', ]))
    def change_rule(self, request):
        request_data = request.data
        user_id = request_data['id']
        try:
            user = User.objects.get(id=user_id)
            if 'is_superuser' in request_data:
                user.is_superuser = request_data['is_superuser']
            if 'is_staff' in request_data:
                user.is_staff = request_data['is_staff']
            if 'is_test_user' in request_data:
                user.is_test_user = request_data['is_test_user']
            user.save()
        except User.DoesNotExist:
            return Response({'success': False, 'message': "User not found"})
        except Exception as e:
            return Response({'success': False, "message": e})
        else:
            return Response({'success': True, "message": "Change successfully"})

    @action(methods=["GET"], detail=True, url_path="rate-limit",
            permission_classes=get_permissions(['admin_user_view', ]))
    def retrieve_rate_limit_info(self, request, *args, **kwargs):
        # user = self.get_queryset().get(id=kwargs['pk'])
        user_id = kwargs['pk']
        current = datetime.datetime.now()
        response_data = []
        try:
            for view_id, view in RATE_LIMIT_VIEW_CHOICES:
                user_rate_limit = retrieve_max_allow_rate_limit(view_id, user_id)

                current_rate_limit_key = "{}{}_{}_{}".format(RATE_LIMIT_PREFIX, view_id, user_id,
                                                             current.strftime("%Y%m%d%H"))
                previous_hour = current - datetime.timedelta(hours=1)
                previous_rate_limit_key = "{}{}_{}_{}".format(RATE_LIMIT_PREFIX, view_id, user_id,
                                                              previous_hour.strftime("%Y%m%d%H"))

                response_data.append({
                    "view": view,
                    "view_id": view_id,
                    "current_rate_limit": get_rate_limit(current_rate_limit_key, user_rate_limit),
                    "previous_rate_limit": get_rate_limit(previous_rate_limit_key, user_rate_limit),
                    "max_rate_limit": user_rate_limit
                })

            return Response({"success": True, "data": response_data})

        except Exception as e:
            logger.error(str(e))
            traceback.print_tb(e.__traceback__)
            return Response({"success": False, "message": str(e)})

    @action(methods=["POST"], detail=True, url_path="update-rate-limit",
            permission_classes=get_permissions(['admin_user_view', ]))
    def update_rate_limit_info(self, request, *args, **kwargs):
        # user = self.get_queryset().get(id=kwargs['pk'])
        user_id = kwargs['pk']
        request_data = request.data
        current = datetime.datetime.now()
        try:
            for rate_limit_data in request_data:
                user_rate_limit = rate_limit_data['max_rate_limit']
                view_id = rate_limit_data['view_id']
                if user_rate_limit:
                    UserLimit.objects.update_or_create(user_id=user_id, view=view_id,
                                                       defaults={"rate_limit": user_rate_limit})

                current_rate_limit_key = "{}{}_{}_{}".format(RATE_LIMIT_PREFIX, view_id, user_id,
                                                             current.strftime("%Y%m%d%H"))
                previous_hour = current - datetime.timedelta(hours=1)
                previous_rate_limit_key = "{}{}_{}_{}".format(RATE_LIMIT_PREFIX, view_id, user_id,
                                                              previous_hour.strftime("%Y%m%d%H"))

                set_rate_limit(current_rate_limit_key, rate_limit_data['current_rate_limit'])
                set_rate_limit(previous_rate_limit_key, rate_limit_data['previous_rate_limit'])

            return Response({"success": True, "data": request_data})

        except Exception as e:
            logger.error(str(e))
            traceback.print_tb(e.__traceback__)
            return Response({"success": False, "message": str(e)})

    @action(methods=['GET'], detail=False, url_path='all/brief')
    def get_all_brief_users(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        return Response(BriefUserSerializer(queryset, many=True).data)

    @action(methods=["POST"], detail=True, url_path="lock_user",
            permission_classes=get_permissions(['admin_update_user', ]))
    def lock_user(self, request,*args, **kwargs):
        user_id = kwargs['pk']
        user = self.queryset.get(pk=user_id)
        user.is_lock = True
        user.save()
        logout_all_device(user_id)
        return Response({'success': True})

    @action(methods=["POST"], detail=True, url_path="unlock_user",
        permission_classes=get_permissions(['admin_update_user', ]))
    def unlock_user(self, request,*args, **kwargs):
        user_id = kwargs['pk']
        user = self.queryset.get(pk=user_id)
        user.is_lock = False
        user.save()
        return Response({'success': True})

    @action(methods=["POST"], detail=True, url_path="confirm_email_user",
        permission_classes=get_permissions(['admin_update_user', ]))
    def confirm_email_user(self, request,*args, **kwargs):
        user_id = kwargs['pk']
        user = self.queryset.get(pk=user_id)
        user.is_email_confirmed = True
        user.save()
        return Response({'success': True})

    @action(methods=["POST"], detail=True, url_path="send_mail_active",
        permission_classes=get_permissions(['admin_update_user', ]))
    def send_mail_active_user(self, request,*args, **kwargs):
        user_id = kwargs['pk']
        send_activation_email_task.delay(user_id=user_id)
        return Response({'success': True})

    @action(methods=["POST"], detail=True, url_path="logout-all-device",
        permission_classes=get_permissions(['admin_update_user', ]))
    def logout_all_device(self, request,*args, **kwargs):
        user_id = kwargs['pk']
        logout_all_device(user_id)
        return Response({'success': True})
