from django.urls import path

from .views import (
    ListCreateJobAPIView,
    RetrieveUpdateDestroyJobAPIView
)

urlpatterns = [
    path('', ListCreateJobAPIView.as_view(), name='list_create_job'),
    path('detail/<str:pk>/', RetrieveUpdateDestroyJobAPIView.as_view(), name='detail_job'),
]
