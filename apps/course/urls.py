from django.urls import path

from .views import (
    ListCreateCourseSectionAPIView,
    RetrieveUpdateDestroyCourseSectionAPIView,
    ListCreateCourseAPIView,
    RetrieveUpdateDestroyCourseAPIView,
)

urlpatterns = [
    path('', ListCreateCourseAPIView.as_view(), name='list_create_course'),
    path('detail/<str:pk>/', RetrieveUpdateDestroyCourseAPIView.as_view(), name='detail_course'),

    path('section/', ListCreateCourseSectionAPIView.as_view(), name='list_create_course_section'),
    path('section/detail/<str:pk>/', RetrieveUpdateDestroyCourseSectionAPIView.as_view(), name='detail_course_section'),
]
