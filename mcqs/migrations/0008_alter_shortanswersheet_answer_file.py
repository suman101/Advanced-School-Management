# Generated by Django 4.0.2 on 2022-02-17 10:08

from django.db import migrations, models
import mcqs.models


class Migration(migrations.Migration):

    dependencies = [
        ('mcqs', '0007_shortanswersheet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortanswersheet',
            name='answer_file',
            field=models.FileField(blank=True, null=True, upload_to=mcqs.models.ShortAnswerSheet.get_upload_path),
        ),
    ]
