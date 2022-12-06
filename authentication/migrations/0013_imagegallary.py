# Generated by Django 4.0.2 on 2022-06-14 09:52

import authentication.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_alter_schoolprofile_phone_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageGallary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=authentication.models.ImageGallary.get_upload_path, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])])),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.schoolprofile')),
            ],
        ),
    ]