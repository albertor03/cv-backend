from django.urls import path

from .views import (
    ListCreateEducationAPIView,
    RetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('', ListCreateEducationAPIView.as_view(), name='list_create_education'),
    path('detail/<str:pk>/', RetrieveUpdateDestroyAPIView.as_view(), name='retrieve_update_destroy_education'),
]
