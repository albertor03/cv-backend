from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import SingUpUserApiView, DetailUserApiView, AllUserApiView

urlpatterns = [
    path('', AllUserApiView.as_view(), name='all_users'),
    path('detail/<str:pk>/', DetailUserApiView.as_view(), name='user_detail'),
    path('sing-up/', SingUpUserApiView.as_view(), name='user_create')
]

urlpatterns = format_suffix_patterns(urlpatterns)
