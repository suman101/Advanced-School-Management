# Generated by Django 4.0.2 on 2022-02-18 11:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import marksheet.models


class Migration(migrations.Migration):

    dependencies = [
        ('marksheet', '0005_marksheet_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marksheet',
            name='exam',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exam_marksheet', to='marksheet.exam'),
        ),
        migrations.AlterField(
            model_name='marksheet',
            name='file',
            field=models.FileField(blank=True, max_length=254, null=True, upload_to=marksheet.models.Marksheet.get_upload_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv'])]),
        ),
    ]