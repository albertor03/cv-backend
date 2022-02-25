from djongo import models


class PersonalInformationModel(models.Model):

    _id = models.ObjectIdField()
    first_name = models.CharField('First Name', max_length=100)
    last_name = models.CharField('Last Name', max_length=100)
    email = models.EmailField('Email')
    profession = models.CharField('Profession', max_length=100)
    phone = models.CharField('Phone', max_length=15, blank=True, null=True)
    address = models.CharField('Address', max_length=100, blank=True, null=True)
    about = models.CharField('About Me', max_length=250)
    created_at = models.DateTimeField('Created at', auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = 'Personal Information'
        verbose_name_plural = "Personal Information's"
        db_table = 'information'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
