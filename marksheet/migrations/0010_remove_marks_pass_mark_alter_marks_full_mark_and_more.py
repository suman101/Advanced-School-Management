# Generated by Django 4.0.2 on 2022-02-21 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marksheet', '0009_remove_marksheet_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marks',
            name='pass_mark',
        ),
        migrations.AlterField(
            model_name='marks',
            name='full_mark',
            field=models.FloatField(default=4),
        ),
        migrations.AlterField(
            model_name='marks',
            name='obtain_mark',
            field=models.FloatField(default=0),
        ),
    ]
