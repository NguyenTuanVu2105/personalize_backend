from rest_framework import mixins

from user.serializers import UserSettingsSerializer


class RetrieveWithUserSettingsModelMixin(mixins.RetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response_data = response.data
        response_data["user_settings"] = UserSettingsSerializer(request.user.settings).data
        return response
