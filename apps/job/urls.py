from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    ListCreateJobAPIView,
    RetrieveUpdateDestroyJobAPIView
)

urlpatterns = [
    path('', ListCreateJobAPIView.as_view(), name='list_create_job'),
    path('detail/<str:pk>/', RetrieveUpdateDestroyJobAPIView.as_view(), name='detail_job'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
