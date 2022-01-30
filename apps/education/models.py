from djongo import models


class EducationModels(models.Model):

    _id = models.ObjectIdField()
    degree = models.CharField('Degree', max_length=100)
    collage = models.CharField('Collage', max_length=100)
    start_date = models.DateField('Start date')
    end_date = models.DateField('End date', null=True, blank=True)
    currently = models.BooleanField('Currently', default=False)
    certificate = models.FileField(upload_to='education', null=True, blank=True)
    created_at = models.DateTimeField('Created at', auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = 'Education'
        verbose_name_plural = "Educations"
        db_table = 'educations'

    def __str__(self):
        return f"{self.degree} in {self.collage}"

    def delete(self, using=None, keep_parents=False):
        self.certificate.storage.delete(self.certificate.name)
        super().delete()