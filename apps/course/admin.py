from django.contrib import admin
from .models import CourseSectionsModel, CoursesModel

admin.site.register([CourseSectionsModel, CoursesModel])
