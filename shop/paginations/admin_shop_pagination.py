from shop.models import ShopTag
from shop.paginations.shop_pagination import ShopPagination


class AdminShopPagination(ShopPagination):
    def get_options(self, queryset):
        options = super(AdminShopPagination, self).get_options(queryset)
        options['tags'] = ShopTag.objects.values_list('tag', flat=True).distinct().order_by()
        return options
