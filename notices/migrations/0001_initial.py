# Generated by Django 4.0.2 on 2022-02-10 15:58

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
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('detail_notice', models.TextField()),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('notice_pdf', models.FileField(max_length=254, upload_to='notice_pdf')),
                ('is_public', models.BooleanField(default=False)),
                ('posted_by', models.ForeignKey(blank=True, limit_choices_to={'user_type': 'NA'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notice_user', to=settings.AUTH_USER_MODEL)),
                ('school', models.ForeignKey(blank=True, limit_choices_to={'user_type': 'SA'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
