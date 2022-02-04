from django.urls import path

from .views import (
    ListCreateCourseSectionAPIView,
    ListCreateCourseAPIView,
    RetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('', ListCreateCourseAPIView.as_view(), name='list_create_course'),
    path('detail/<str:pk>/', RetrieveUpdateDestroyAPIView.as_view(), name='detail_course'),

    path('section/', ListCreateCourseSectionAPIView.as_view(), name='list_create_course_section'),
]
