# Generated by Django 3.2.11 on 2022-02-10 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('grade_and_subject', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='class_teacher',
            field=models.ForeignKey(blank=True, limit_choices_to={'user_type': 'TE'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teacher_grade', to='authentication.teacherprofile'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='school',
            field=models.ForeignKey(limit_choices_to={'user_type': 'SA'}, on_delete=django.db.models.deletion.CASCADE, related_name='school_grade', to='authentication.schoolprofile'),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='school',
            field=models.ForeignKey(limit_choices_to={'user_type': 'SA'}, on_delete=django.db.models.deletion.CASCADE, related_name='school_subjects', to='authentication.schoolprofile'),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='subject_teacher',
            field=models.ForeignKey(blank=True, limit_choices_to={'user_type': 'TE'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teacher_subjects', to='authentication.teacherprofile'),
        ),
    ]
