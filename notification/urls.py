from django.urls import path, include
from rest_framework import routers

from notification.views import SellerEmail
from notification.views.instant_prompt import InstantPromptViewSet
from notification.views.mail_history import MailHistoryViewSet
from notification.views.message import MessageViewSet
from notification.views.seller_email import SellerEmailSupportedAggregate
from notification.views.template import NotificationTemplateViewSet
from notification.viewsets.order_tracking_notification import OrderTrackingNotificationViewSet

message_router = routers.DefaultRouter()
message_router.register(r'', MessageViewSet)

template_router = routers.DefaultRouter()
template_router.register(r'', NotificationTemplateViewSet)

mailhistory_router = routers.DefaultRouter()
mailhistory_router.register(r'', MailHistoryViewSet)

instant_prompt_router = routers.DefaultRouter()
instant_prompt_router.register(r'', InstantPromptViewSet)

order_tracking_router = routers.DefaultRouter()
order_tracking_router.register(r'', OrderTrackingNotificationViewSet)

urlpatterns = [
    path('message/', include(message_router.urls)),
    path('notification-template/', include(template_router.urls)),
    path('mail-history/', include(mailhistory_router.urls)),
    path('instant_prompt/', include(instant_prompt_router.urls)),
    path('order-tracking-notification/', include(order_tracking_router.urls)),
    path('custom-email/', SellerEmail.as_view()),
    path('custom-email/supported-agg/', SellerEmailSupportedAggregate.as_view())
]
