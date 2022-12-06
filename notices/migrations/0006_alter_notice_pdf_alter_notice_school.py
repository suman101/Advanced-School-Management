# Generated by Django 4.0.2 on 2022-02-10 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('notices', '0005_alter_notice_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='pdf',
            field=models.FileField(max_length=254, upload_to='notice_pdf'),
        ),
        migrations.AlterField(
            model_name='notice',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.schoolprofile'),
        ),
    ]