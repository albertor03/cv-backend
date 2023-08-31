from djongo import models


class CoursesModel(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField('Course name', max_length=100)
    company = models.CharField('Company name', max_length=150)
    end_date = models.DateField('End Date')
    certificate = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField('Created at', auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = "Courses"
        db_table = 'courses'

    def __str__(self):
        return f"{self.name} in {self.company}"


class CourseSectionsModel(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField('Course name', max_length=100)
    courses = models.ArrayReferenceField(
        to=CoursesModel,
        null=True,
        blank=True,
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
            CoursesModel.objects.filter(_id=course.pk).first().delete()

        super().delete()
