# Generated by Django 4.0.2 on 2022-02-10 08:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import researchs.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=110)),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=50, null=True)),
                ('school', models.ForeignKey(limit_choices_to={'user_type': 'SA'}, on_delete=django.db.models.deletion.CASCADE, related_name='school_subject', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ResearchDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=250)),
                ('published_by', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(null=True)),
                ('link', models.URLField(max_length=100)),
                ('pdf', models.FileField(blank=True, max_length=254, null=True, upload_to=researchs.models.ResearchDetail.get_upload_path)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('approved', models.BooleanField(default=True)),
                ('publish', models.BooleanField(default=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='researchs.category')),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.schoolprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]