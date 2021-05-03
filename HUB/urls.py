"""HUB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from HUB.views.auth import obtain_jwt_token, obtain_jwt_staff_token, obtain_jwt_token_logout, \
    obtain_jwt_token_by_refresh_token
from abstract_product.urls import urlpatterns as product_urlpatterns
from analytics.urls import urlpatterns as analytic_urlpatterns
from billing.sub_apps.braintree_payment.urls import urlpatterns as braintree_urlpatterns
from billing.sub_apps.combine_payment.urls import urlpatterns as combine_payment_urlpatterns
from billing.sub_apps.payoneer_payment.urls import urlpatterns as payoneer_urlpatterns
from billing.sub_apps.paypal_payment.urls import urlpatterns as paypal_urlpatterns
from billing.sub_apps.paypal_vault_payment.urls import urlpatterns as paypal_vault_urlpatterns
from billing.sub_apps.stripe_payment.urls import urlpatterns as stripe_urlpatterns
from billing.urls import urlpatterns as billing_urlpatterns
from notification.urls import urlpatterns as notification_urlpatterns
from order.urls import fulfill_service_hook_urlpatterns
from order.urls import urlpatterns as order_urlpatterns
from service_communication.urls import urlpatterns as service_communication_url
from shipping.urls import urlpatterns as shipping_urlpatterns
from shop.urls import urlpatterns as shop_urlpatterns
from support.urls import urlpatterns as support_urlpatterns
from system_metadata.urls import urlpatterns as system_metadata_url
from user.urls import urlpatterns as seller_urlpatterns
from user.views import CreateUserView
from user_product.urls import urlpatterns as user_product_urlpatterns
from coupon.urls import urlpatterns as coupon_urlpatterns
from statistic.urls import urlpatterns as product_statistic_urlpatterns
from admin_tools.urls import urlpatterns as admin_tools_urlpatterns
from event.urls import urlpatterns as event_urlpatterns

api__urlpatterns = [
    path('/', include(product_urlpatterns)),
    path('/', include(notification_urlpatterns)),
    path('/', include(seller_urlpatterns)),
    path('/', include(order_urlpatterns)),
    path('/', include(shop_urlpatterns)),
    path("/", include(service_communication_url)),
    path("/", include(billing_urlpatterns)),
    path('/', include(stripe_urlpatterns)),
    path('/', include(braintree_urlpatterns)),
    path('/', include(combine_payment_urlpatterns)),
    path('/', include(notification_urlpatterns)),
    path('/', include(user_product_urlpatterns)),
    path('/', include(shipping_urlpatterns)),
    path('/', include(system_metadata_url)),
    path('/', include(analytic_urlpatterns)),
    path('/', include(payoneer_urlpatterns)),
    path('/', include(paypal_urlpatterns)),
    path('/', include(paypal_vault_urlpatterns)),
    path('/', include(support_urlpatterns)),
    path('/', include(coupon_urlpatterns)),
    path('/', include(event_urlpatterns)),
    path('/auth/', include('rest_framework.urls')),
    path('/token-auth/', obtain_jwt_token),
    path('/staff-token-auth/', obtain_jwt_staff_token),
    path('/register/', CreateUserView.as_view(), name='register'),
    # path('/activate/<str:uidb64>/<str:token>', AccountActivation.as_view()),
    path('/accounts/', include('django.contrib.auth.urls')),
    path('/token-logout/', obtain_jwt_token_logout),
    path('/token/', obtain_jwt_token_by_refresh_token),
    path('/', include(product_statistic_urlpatterns)),
    path('/admin/tools/', include(admin_tools_urlpatterns)),
]

internal__urlpatterns = [
    path('/', include(fulfill_service_hook_urlpatterns)),
]

urlpatterns = [
    path('api/v1', include(api__urlpatterns)),
    path('internal', include(internal__urlpatterns)),
]

if settings.ADMIN_ENABLED:
    urlpatterns.append(path('admin/', admin.site.urls))
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

# route static for gunicorn
urlpatterns += staticfiles_urlpatterns()

if settings.USE_LOCAL_STORAGE is not None and settings.USE_LOCAL_STORAGE:
    urlpatterns = urlpatterns + static(settings.MEDIA_CONTEXT_PATH, document_root=settings.MEDIA_ROOT)
