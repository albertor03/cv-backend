from django.urls import path

from .views import (
    ListCreateCourseSectionAPIView,
    ListCreateCourseAPIView, RetrieveUpdateDestroyCourseSectionAPIView,
)

urlpatterns = [
    path('', ListCreateCourseAPIView.as_view(), name='list_create_course'),

    path('section/', ListCreateCourseSectionAPIView.as_view(), name='list_create_course_section'),
    path('section/detail/<str:pk>/', RetrieveUpdateDestroyCourseSectionAPIView.as_view(), name='detail_course_section'),
]
