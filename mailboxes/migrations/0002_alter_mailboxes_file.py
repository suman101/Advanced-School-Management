# Generated by Django 4.0.2 on 2022-03-21 07:27

from django.db import migrations, models
import mailboxes.models


class Migration(migrations.Migration):

    dependencies = [
        ('mailboxes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailboxes',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=mailboxes.models.get_upload_path),
        ),
    ]
