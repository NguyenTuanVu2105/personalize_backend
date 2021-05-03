from django.apps import AppConfig


class ServiceCommunicationConfig(AppConfig):
    name = 'service_communication'

    def ready(self):
        import service_communication.services.adapter_services.callbacks
