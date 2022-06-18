from bson import ObjectId
from djongo import models

from cloudinary_storage.storage import RawMediaCloudinaryStorage


class CoursesModel(models.Model):

    _id = models.ObjectIdField()
    name = models.CharField('Course name', max_length=100)
    company = models.CharField('Company name', max_length=150)
    end_date = models.DateField('End Date')
    certificate = models.FileField(upload_to='course', null=True, storage=RawMediaCloudinaryStorage())
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField('Created at', auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = "Courses"
        db_table = 'courses'

    def __str__(self):
        return f"{self.name} in {self.company}"

    def delete(self, using=None, keep_parents=False):
        if self.certificate.name:
            self.certificate.storage.delete(self.certificate.name)
        super().delete()


class CourseSectionsModel(models.Model):

    _id = models.ObjectIdField()
    name = models.CharField('Course name', max_length=100)
    courses = models.ArrayReferenceField(
        to=CoursesModel,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField('Created at', auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True, auto_now_add=False)

    objects = models.DjongoManager()

    class Meta:
        verbose_name = 'Course Section'
        verbose_name_plural = "Courses Section"
        db_table = 'courses-section'

    def __str__(self):
        return f"{self.name}"

    def delete(self, using=None, keep_parents=False):
        for course in list(self.courses.all()):
            CoursesModel.objects.filter(_id=course.pk).first().delete(True)

        super().delete()
