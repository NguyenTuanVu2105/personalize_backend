from django.apps import AppConfig


class UserProductConfig(AppConfig):
    name = 'user_product'

    def ready(self):
        import user_product.signals

        import user_product.functions.callbacks
