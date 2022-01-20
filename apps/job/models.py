from djongo import models


class JobModels(models.Model):

    _id = models.ObjectIdField()
    position = models.CharField('Position', max_length=100)
    company_name = models.CharField('Company Name', max_length=100)
    start_date = models.DateTimeField('Start Date')
    end_date = models.DateTimeField('Start Date', blank=True, null=True)
    currently = models.BooleanField(default=False)
    address = models.CharField('Address', max_length=100)
    created_at = models.DateTimeField('Created at', auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = "Jobs"
        db_table = 'jobs'

    def __str__(self):
        return f"{self.position} {self.company_name}"
