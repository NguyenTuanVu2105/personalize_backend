from rest_framework.serializers import ModelSerializer

from event.models import EventTemplate


class EventTemplateSerializer(ModelSerializer):
    class Meta:
        model = EventTemplate
        fields = '__all__'


class BriefEventTemplateSerializer(ModelSerializer):
    class Meta:
        model = EventTemplate
        fields = ('name', 'start_time', 'end_time', 'status', 'header_html', )
