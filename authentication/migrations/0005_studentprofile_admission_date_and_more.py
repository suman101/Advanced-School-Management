# Generated by Django 4.0.2 on 2022-02-19 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_studentprofile_caste_studentprofile_religion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='admission_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='teacherprofile',
            name='joined_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
