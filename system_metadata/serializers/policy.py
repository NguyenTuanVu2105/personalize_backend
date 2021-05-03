from rest_framework.serializers import ModelSerializer

from system_metadata.models import Policy


class PolicySerializer(ModelSerializer):
    class Meta:
        model = Policy
        fields = ['id', 'title', 'content', 'last_updated_content', 'sort_index', 'is_prompt', 'is_active']


class BriefPolicySerializer(ModelSerializer):
    class Meta:
        model = Policy
        fields = ['id', 'title', 'is_prompt', 'update_time', 'is_active']
