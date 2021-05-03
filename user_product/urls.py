from django.urls import path, include
from rest_framework import routers

from user_product.views import ArtworkCheckView, NoArtworkUserVariantCreateView, UserProductCheckView, \
    BackgroundCustomizeDataGeneratorView
from user_product.viewsets.artwork_chunks import ArtworkChunkViewSet
from .views import UserVariantCreateView, RecentUsedProductView, MockupPreviewDataGeneratorView, AdminArtworkDefault, \
    AdminProduct
from .views.adapter_service_product import ProductServiceAdapterViewSet
from .viewsets import ArtworkViewSet, UserProductViewSet, UserAbstractVariantDefaultPriceViewSet, ArtworkHistoryViewSet, \
    SampleProductViewSet, AdminProductViewSet, AdminSampleProductViewSet, UserFontFamilyViewSet, AdminFontFamilyViewSet
from .viewsets.ecommerce_unsync_product import EcommerceUnsyncProductViewSet
from .viewsets.uploaded_mockup import UploadedMockupViewSet

seller_router = routers.DefaultRouter()
seller_router.register(r'user-product', UserProductViewSet)
seller_router.register(r'artworks', ArtworkViewSet)
seller_router.register(r'artwork_chunks', ArtworkChunkViewSet)
seller_router.register(r'variant-default-price', UserAbstractVariantDefaultPriceViewSet)
seller_router.register(r'artwork-history', ArtworkHistoryViewSet)
seller_router.register(r'ecommerce-unsync-product', EcommerceUnsyncProductViewSet)
seller_router.register(r'sample-product', SampleProductViewSet)
seller_router.register(r'font', UserFontFamilyViewSet)

service_router = routers.DefaultRouter()
service_router.register(r'uploaded-mockup', UploadedMockupViewSet)

admin_router = routers.DefaultRouter()
admin_router.register(r'admin-product', AdminProductViewSet)
admin_router.register(r'admin-sample', AdminSampleProductViewSet)
admin_router.register(r'font', AdminFontFamilyViewSet)

admin_artworks_default_router = routers.DefaultRouter()
admin_artworks_default_router.register(r'', AdminArtworkDefault)

admin_product_router = routers.DefaultRouter()
admin_product_router.register(r'', AdminProduct)

product_adapter_service = routers.DefaultRouter()
product_adapter_service.register(r'', ProductServiceAdapterViewSet)
seller_urlpatterns = [
    path('variants/', UserVariantCreateView.as_view()),
    path('no-artwork-variants/', NoArtworkUserVariantCreateView.as_view()),
    # path('preview-mockup/', PreviewMockupView.as_view()),
    path('artwork-check/', ArtworkCheckView.as_view()),
    path('product-check/', UserProductCheckView.as_view()),
    path('product-recent-used/', RecentUsedProductView.as_view()),
]

service_urlpatterns = [
    path('mockup-data/', MockupPreviewDataGeneratorView.as_view()),
    path('background-custom/', BackgroundCustomizeDataGeneratorView.as_view()),
]

urlpatterns = [
    path('admin/', include(admin_router.urls)),
    path('seller/', include(seller_router.urls)),
    path('service/', include(service_router.urls)),
    path('seller/', include(seller_urlpatterns)),
    path('service/', include(service_urlpatterns)),
    path('hook/products/', include(product_adapter_service.urls)),
    path('admin/default_artwork/', include(admin_artworks_default_router.urls)),
    path('admin/abstract_products/', include(admin_product_router.urls))
]
