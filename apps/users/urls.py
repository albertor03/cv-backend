from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    SingUpUserApiView,
    DetailUserApiView,
    AllUserApiView,
    LoginAPIView,
    LogoutAPIView
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', AllUserApiView.as_view(), name='all_users'),
    path('detail/<str:pk>/', DetailUserApiView.as_view(), name='user_detail'),
    path('sing-up/', SingUpUserApiView.as_view(), name='user_create'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
