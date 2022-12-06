# Generated by Django 3.2.11 on 2022-02-09 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=50, null=True)),
                ('school', models.ForeignKey(limit_choices_to={'user_type': 'SA'}, on_delete=django.db.models.deletion.CASCADE, related_name='school_subjects', to=settings.AUTH_USER_MODEL)),
                ('subject_teacher', models.ForeignKey(blank=True, limit_choices_to={'user_type': 'TE'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teacher_subjects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('grade_name', models.CharField(choices=[('Nursery', 'Nursery'), ('L.K.G', 'L.K.G'), ('U.K.G', 'U.K.G'), ('One', 'One(1)'), ('Two', 'Two(2)'), ('Three', 'Three(3)'), ('Four', 'Four(4)'), ('Five', 'Five(5)'), ('Six', 'Six(6)'), ('Seven', 'Seven(7)'), ('Eight', 'Eight(8)'), ('Nine', 'Nine(9)'), ('Ten', 'Ten(10)'), ('Eleven', 'Eleven(11)'), ('Twelve', 'Twelve(12)')], default='One', max_length=10)),
                ('section', models.CharField(default='A', max_length=10)),
                ('class_teacher', models.ForeignKey(blank=True, limit_choices_to={'user_type': 'TE'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teacher_grade', to=settings.AUTH_USER_MODEL)),
                ('school', models.ForeignKey(limit_choices_to={'user_type': 'SA'}, on_delete=django.db.models.deletion.CASCADE, related_name='school_grade', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ManyToManyField(to='grade_and_subject.Subjects')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
