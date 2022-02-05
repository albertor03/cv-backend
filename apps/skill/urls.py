from django.urls import path

from .views import (
    ListCreateSkillAPIView,
    RetrieveUpdateDestroySkillAPIView
)

urlpatterns = [
    path('', ListCreateSkillAPIView.as_view(), name='list_create_skill'),
    path('detail/<str:pk>/', RetrieveUpdateDestroySkillAPIView.as_view(), name='retrieve_update_destroy_skill'),
]
