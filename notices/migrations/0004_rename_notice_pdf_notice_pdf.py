# Generated by Django 4.0.2 on 2022-02-10 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0003_notice_notice_pdf'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notice',
            old_name='notice_pdf',
            new_name='pdf',
        ),
    ]
