from bson import ObjectId
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
        new_courses = list()
        section_id_to_update = str()
        if self.certificate.name:
            self.certificate.storage.delete(self.certificate.name)

        if using is None:
            sections = CourseSectionsModel.objects.all()
            for section in sections:
                for course in section.courses:
                    if course['_id'] != self._id:
                        new_courses.append(course)
                        section_id_to_update = section.pk

            section_to_update = CourseSectionsModel.objects.filter(_id=ObjectId(section_id_to_update)).first()
            section_to_update.courses = new_courses
            section_to_update.save()

        super().delete()


class CourseSectionsModel(models.Model):

    _id = models.ObjectIdField()
    name = models.CharField('Course name', max_length=100)
    courses = models.ArrayField(model_container=CoursesModel, null=True, blank=True)
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
        for course in self.courses:
            CoursesModel.objects.filter(_id=ObjectId(course['_id'])).first().delete(True)

        super().delete()
