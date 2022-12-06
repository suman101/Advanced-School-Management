# Generated by Django 4.0.2 on 2022-03-26 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_alter_schoolprofile_phone_number_and_more'),
        ('posts', '0006_merge_20220223_1140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='responsed_by',
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='authentication.teacherprofile'),
        ),
    ]
