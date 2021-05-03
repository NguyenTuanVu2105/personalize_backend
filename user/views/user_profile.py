from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.exceptions.FormValidationError import FormValidationError
from HUB.viewsets.base import AuthenticatedGenericViewSet
from user.contants import AccountType
from user.serializers import ChangePasswordSerializer, UserProfileSerializer
from ..forms.user_update_form import UserUpdateForm
from ..serializers import UserSerializer

User = get_user_model()


class UserProfileViewSet(AuthenticatedGenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    error_messages = {
        "user": {
            "invalid": "This user is invalid",
            "required": "User is required"
        },
        "password": {
            "incorrect": "This password is incorrect",
            "invalid": "Password is invalid",
        },
        "gender": {
            "invalid_choice": "Gender is invalid"
        }
    }

    @action(methods=["POST"], detail=False, url_path="change-password")
    def change_password(self, request):
        request_data = request.data
        serializer = ChangePasswordSerializer(data=request_data)
        if not serializer.is_valid():
            raise FormValidationError(field="password", code="invalid")
        user = self.request.user
        new_password = request_data['new_password']
        if user.account_type == AccountType.GOOGLE and user.last_change_password is None:
            user.set_password(new_password)
        else:
            old_password = request_data['old_password']
            if not user.check_password(old_password):
                raise FormValidationError(field="password", code="incorrect")
            user.set_password(new_password)
        user.last_change_password = timezone.now()
        user.save()
        return Response({"success": True, "message": "Change password successfully"})

    @action(methods=["GET"], detail=False, url_path="info")
    def profile(self, request):
        user = User.objects.get(id=self.request.user.pk)
        return Response({"success": True, "profile": UserProfileSerializer(instance=user).data})

    @action(methods=["PUT"], detail=False, url_path="update-info")
    def update_profile(self, request):
        request_data = request.data
        user = User.objects.get(id=self.request.user.pk)
        form = UserUpdateForm(instance=user, data=request_data)
        form.validate()
        user = form.save()
        return Response({"success": True, "profile": UserProfileSerializer(instance=user).data})

    @action(methods=["PUT"], detail=False, url_path="update-message")
    def update_message(self, request):
        request_data = request.data
        user = User.objects.get(id=self.request.user.pk)
        if 'message_id' in request_data:
            user.message_id = request_data['message_id']
        user.save()
        return Response({"success": True, "message_id": user.message_id})
