from django.apps import AppConfig


class OrderConfig(AppConfig):
    name = 'order'

    def ready(self):
        import order.signals

        import order.services.callbacks
