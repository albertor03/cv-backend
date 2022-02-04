from djongo import models

from cloudinary_storage.storage import RawMediaCloudinaryStorage


class CoursesModel(models.Model):

    _id = models.ObjectIdField()
    name = models.CharField('Course name', max_length=100)
    company = models.CharField('Company name', max_length=150)
    end_date = models.DateField('End Date')
    certificate = models.FileField(upload_to='course', null=True, storage=RawMediaCloudinaryStorage())
    created_at = models.DateTimeField('Created at', auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = "Courses"
        db_table = 'courses'

    def __str__(self):
        return f"{self.name} in {self.company}"

    def delete(self, using=None, keep_parents=False):
        self.certificate.storage.delete(self.certificate.name)
        super().delete()


class CourseSectionsModel(models.Model):

    _id = models.ObjectIdField()
    name = models.CharField('Course name', max_length=100)
    courses = models.ArrayField(model_container=CoursesModel, null=True, blank=True)
    created_at = models.DateTimeField('Created at', auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True, auto_now_add=False)

    object = models.DjongoManager()

    class Meta:
        verbose_name = 'Course Section'
        verbose_name_plural = "Courses Section"
        db_table = 'courses-section'

    def __str__(self):
        return f"{self.name}"
