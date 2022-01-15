from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PersonalInformationAPIView, PersonalInformationDetailAPIView

urlpatterns = [
    path('', PersonalInformationAPIView.as_view(), name='info'),
    path('detail/<str:pk>/', PersonalInformationDetailAPIView.as_view(), name='info_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
