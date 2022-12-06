# Generated by Django 4.0.2 on 2022-02-16 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_studentprofile_grade'),
        ('marksheet', '0004_alter_marksheet_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='marksheet',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='std_marksheet', to='authentication.studentprofile'),
        ),
    ]