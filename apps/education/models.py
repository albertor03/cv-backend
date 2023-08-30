from djongo import models

from cloudinary_storage.storage import RawMediaCloudinaryStorage


class EducationModels(models.Model):

    _id = models.ObjectIdField()
    degree = models.CharField('Degree', max_length=100)
    collage = models.CharField('Collage', max_length=100)
    start_date = models.DateField('Start date')
    end_date = models.DateField('End date', null=True, blank=True)
    currently = models.BooleanField('Currently', default=False)
    certificate = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField('Created at', auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = 'Education'
        verbose_name_plural = "Educations"
        db_table = 'educations'

    def __str__(self):
        return f"{self.degree} in {self.collage}"
