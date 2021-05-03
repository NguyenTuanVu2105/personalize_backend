from django.urls import path, include
from rest_framework import routers

from .views.ticket_conversation_view import TicketConversationViewSet
from .views.ticket_update_hook_view import TicketUpdateHookView
from .views.user_ticket_support_view import UserTicketSupportView

user_ticket_support_router = routers.DefaultRouter()
user_ticket_support_router.register(r'', UserTicketSupportView)
ticket_conversation_router = routers.DefaultRouter()
ticket_conversation_router.register(r'', TicketConversationViewSet)
urlpatterns = [
    path('support/ticket/hook/', TicketUpdateHookView.as_view()),
    path('support/ticket/', include(user_ticket_support_router.urls)),
    path('support/conversations/', include(ticket_conversation_router.urls)),
]
