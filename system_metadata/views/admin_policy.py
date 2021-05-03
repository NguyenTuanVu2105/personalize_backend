import logging
import traceback

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.permissions import get_permissions, method_permission_required
from HUB.viewsets.base import AuthenticatedGenericViewSet
from helper.string_helpers import remove_unsafe_html_elements
from notification.enums.instant_prompt_types import InstantPromptType
from notification.functions import renew_instant_prompt
from system_metadata.forms.policy import PolicyForm
from system_metadata.models import Policy
from system_metadata.serializers import PolicySerializer, BriefPolicySerializer

logger = logging.getLogger(__name__)


class AdminPolicyViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         AuthenticatedGenericViewSet):
    serializer_class = PolicySerializer
    queryset = Policy.objects.all()

    @method_permission_required(get_permissions(['admin_policy_view', ]))
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(BriefPolicySerializer(queryset, many=True).data)

    @method_permission_required(get_permissions(['admin_policy_create', ]))
    def create(self, request, *args, **kwargs):
        try:
            request_data = request.data
            policy_form = PolicyForm(data={
                **request_data,
                "sort_index": len(self.get_queryset()) + 1
            })
            policy_form.validate()
            policy_obj = policy_form.save()

            if request_data['is_renew']:
                renew_instant_prompt(InstantPromptType.POLICY_AGREEMENT)

            return Response({"success": True, "policy_id": policy_obj.id})

        except Exception as e:
            traceback.print_tb(e.__traceback__)
            logger.info(str(e))
            return Response({"success": False, "message": str(e)})

    @method_permission_required(get_permissions(['admin_policy_update', ]))
    def update(self, request, *args, **kwargs):
        try:
            request_data = request.data
            policy = self.get_object()
            policy.title = request_data['title']
            policy.content = remove_unsafe_html_elements(request_data['content'])
            policy.last_updated_content = remove_unsafe_html_elements(request_data['last_updated_content'])
            policy.is_prompt = request_data['is_prompt']
            policy.save()

            if request_data['is_renew']:
                renew_instant_prompt(InstantPromptType.POLICY_AGREEMENT)

            return Response({"success": True, "policy_id": policy.id})

        except Exception as e:
            traceback.print_tb(e.__traceback__)
            logger.info(str(e))
            return Response({"success": False, "message": str(e)})

    @method_permission_required(get_permissions(['admin_policy_update', ]))
    def destroy(self, request, *args, **kwargs):
        policy = self.get_object()
        policy.is_active = False
        policy.save()
        return Response({"success": True})

    @action(methods=["PUT"], detail=True, url_path="active",
            permission_classes=get_permissions(['admin_policy_update']))
    def active_policy(self, request, *args, **kwargs):
        policy = self.get_object()
        policy.is_active = True
        policy.save()
        return Response({"success": True})

    @action(methods=["PUT"], detail=False, url_path="reorder",
            permission_classes=get_permissions(['admin_policy_update']))
    def reorder_policy(self, request, *args, **kwargs):
        request_data = request.data
        try:
            policies = request_data['policies']
            for index, policy_data in enumerate(policies):
                policy = Policy.objects.get(id=policy_data['id'])
                policy.sort_index = index + 1
                policy.save()
        except Exception as e:
            print(str(e))
            return Response({"success": False, "message": str(e)})
        else:
            return Response({"success": True, "message": "Reorder policy successfully"})

    @action(methods=["GET"], detail=False, url_path="list-prompt")
    def list_prompt(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(is_prompt=True)
        return Response(PolicySerializer(queryset, many=True).data)
