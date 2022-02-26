from djongo import models


class SkillModel(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField('Skill name', max_length=100)
    percentage = models.FloatField('Percentage')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField('Created at', auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = "Skills"
        db_table = 'skills'

    def __str__(self):
        return f"{self.name} about {self.percentage}"
