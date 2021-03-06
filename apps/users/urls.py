from django.urls import path

from .views import (
    SingUpUserApiView,
    DetailUserApiView,
    AllUserApiView,
    LoginAPIView,
    LogoutAPIView,
    ResetPasswordOfLoggedInUserAPIView,
    ActiveUserAPIView,
    SendActivateLinkAPIView, SendResetPasswordLinkAPIView
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('sing-up/', SingUpUserApiView.as_view(), name='user_create'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', AllUserApiView.as_view(), name='all_users'),
    path('detail/<str:pk>/', DetailUserApiView.as_view(), name='user_detail'),

    path('reset-passoword/', ResetPasswordOfLoggedInUserAPIView.as_view(), name='reset_password_of_user_logged'),
    path('active-user/<str:token>', ActiveUserAPIView.as_view(), name='active_user'),
    path('send-active-user-link/', SendActivateLinkAPIView.as_view(), name='send-activate-user-link'),
    path('send-reset-password-link/', SendResetPasswordLinkAPIView.as_view(), name='send-reset-password-link'),
]
