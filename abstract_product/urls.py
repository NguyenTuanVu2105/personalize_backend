from django.urls import path, include
from rest_framework import routers

from abstract_product.views import CategoryReorder, ProductDataImport, CutImageAPIView, CutImageUploadAPIView, \
    ModelFileAPIView, ModelFileUploadChunkAPIView, ModelFileMergeChunkAPIView, SampleMockupBackgroundAPIView, \
    AdminSampleMockupBackgroundAPIView
from abstract_product.viewsets import AdminProductAttributeValue, AbstractProductCategoryViewSet, \
    AbstractProductViewSet, AbstractProductSideViewSet, FFMProductInfoViewSet
from abstract_product.viewsets.admin_abstract_product import AdminAbstractProductViewSet
from abstract_product.viewsets.admin_abstract_product_category import AdminAbstractProductCategoryViewSet
from abstract_product.viewsets.admin_mockup_info import AdminMockupInfoViewSet

product_router = routers.DefaultRouter()
product_router.register(r'product-categories', AbstractProductCategoryViewSet)
product_router.register(r'admin/product-categories', AdminAbstractProductCategoryViewSet)
product_router.register(r'products', AbstractProductViewSet)
product_router.register(r'admin/products', AdminAbstractProductViewSet)
product_router.register(r'side', AbstractProductSideViewSet)
product_router.register(r'admin/attribute-value', AdminProductAttributeValue)
product_router.register(r'mockup', AdminMockupInfoViewSet)
product_router.register(r'ffm-product-info', FFMProductInfoViewSet)

urlpatterns = [
    path('abstract/', include(product_router.urls)),
    path('abstract/category-reorder', CategoryReorder.as_view()),
    path('abstract/product-import', ProductDataImport.as_view()),
    path('abstract/mockup-info/cut-image/', CutImageAPIView.as_view()),
    path('abstract/mockup-info/cut-image/upload/', CutImageUploadAPIView.as_view()),
    path('abstract/mockup-info/model-file/', ModelFileAPIView.as_view()),
    path('abstract/mockup-info/model-file/chunk/upload/', ModelFileUploadChunkAPIView.as_view()),
    path('abstract/mockup-info/model-file/chunk/merge/', ModelFileMergeChunkAPIView.as_view()),
    path('abstract/sample-mockup-background/', SampleMockupBackgroundAPIView.as_view()),
    path('admin/sample-mockup-background/', AdminSampleMockupBackgroundAPIView.as_view()),
]
