# Generated by Django 3.2.6 on 2022-02-25 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_jobmodels_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobmodels',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]