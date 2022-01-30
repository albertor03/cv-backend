from django.urls import path

from .views import PersonalInformationAPIView, PersonalInformationDetailAPIView

urlpatterns = [
    path('', PersonalInformationAPIView.as_view(), name='info'),
    path('detail/<str:pk>/', PersonalInformationDetailAPIView.as_view(), name='info_detail'),
]
