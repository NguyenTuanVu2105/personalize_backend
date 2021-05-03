from rest_framework import mixins

from user.serializers import UserSettingsSerializer


class ListWithUserSettingsModelMixin(mixins.ListModelMixin):
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response_data = response.data
        response_data["user_settings"] = UserSettingsSerializer(request.user.settings).data
        return response
