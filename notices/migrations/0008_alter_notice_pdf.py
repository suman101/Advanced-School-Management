# Generated by Django 4.0.2 on 2022-03-03 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0007_remove_notice_posted_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='pdf',
            field=models.FileField(blank=True, max_length=254, null=True, upload_to='notice_pdf'),
        ),
    ]