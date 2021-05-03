from django.urls import path, include
from rest_framework import routers

from user.views import AccountActivation, ForgotPasswordView
from user.views.reset_password import ResetPasswordView
from .views import UserProfileViewSet, GoogleAuthView, SendActivationEmail
from .views.token_auth import TokenAuthView
from .views.user_admin import AdminUserViewSet
from .viewsets import UserViewSet, UserSettingsViewSet, UserTagViewSet
from .viewsets.admin_user_settings_view_sets import AdminUserSettingsViewSet

seller_router = routers.DefaultRouter()
seller_router.register(r'info', UserViewSet)
seller_router.register(r'settings', UserSettingsViewSet)

admin_user_settings_router = routers.DefaultRouter()
admin_user_settings_router.register(r'', AdminUserSettingsViewSet)

profile_router = routers.DefaultRouter()
profile_router.register(r'', UserProfileViewSet, base_name='user-profile')

admin_router = routers.DefaultRouter()
admin_router.register(r'', AdminUserViewSet)

user_tag_router = routers.DefaultRouter()
user_tag_router.register(r'', UserTagViewSet)

seller_urlpatterns = [
    path('google-auth/', GoogleAuthView.as_view()),
    path('account-activation/', SendActivationEmail.as_view()),
    path('activate-account/', AccountActivation.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
]

token_auth_urlpatterns = [
    path('token-auth/', TokenAuthView.as_view()),
]

urlpatterns = [
    path('user/', include(token_auth_urlpatterns)),
    path('seller/', include(seller_router.urls)),
    path('seller/', include(seller_urlpatterns)),
    path('seller/profile/', include(profile_router.urls)),
    path('admin/users/', include(admin_router.urls)),
    path('admin/user-tags/', include(user_tag_router.urls)),
    path('admin/user-settings/', include(admin_user_settings_router.urls))
]
