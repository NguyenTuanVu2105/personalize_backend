import re

from rest_framework import mixins

from user.queries import RawSearchQuery
from user.serializers import UserSettingsSerializer


class SearchableListModelMixin(mixins.ListModelMixin):

    def list(self, request, *args, **kwargs):
        q = request.query_params.get("q")
        if q:
            q = re.sub(r'[!\'()|&<>:*\[\];$\"]', ' ', q).strip()
            q = re.sub(r'\s+', ' & ', q)
            if q.strip():
                q += ':*'
                self.queryset = self.get_queryset().filter(tsv_metadata_search=RawSearchQuery(q))
        return super().list(request, *args, **kwargs)


class SearchableListModelMixinWithUserSetting(SearchableListModelMixin):
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response_data = response.data
        response_data["user_settings"] = UserSettingsSerializer(request.user.settings).data
        return response