# Generated by Django 4.0.2 on 2022-03-24 10:27

import annual_report.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('grade_and_subject', '0011_remove_grade_class_teacher'),
        ('authentication', '0012_alter_schoolprofile_phone_number_and_more'),
        ('marksheet', '0011_alter_marksheet_exam_alter_marksheet_grade'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(blank=True, max_length=254, null=True, upload_to=annual_report.models.Report.get_upload_path)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marksheet.exam')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grade_and_subject.grade')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.schoolprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
