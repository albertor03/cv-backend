# Generated by Django 3.2.6 on 2022-02-25 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_alter_educationmodels_certificate'),
    ]

    operations = [
        migrations.AddField(
            model_name='educationmodels',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
