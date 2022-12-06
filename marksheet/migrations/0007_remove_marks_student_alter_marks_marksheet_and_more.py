# Generated by Django 4.0.2 on 2022-02-19 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marksheet', '0006_alter_marksheet_exam_alter_marksheet_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marks',
            name='student',
        ),
        migrations.AlterField(
            model_name='marks',
            name='marksheet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mark_marksheet', to='marksheet.marksheet'),
        ),
        migrations.AlterField(
            model_name='marks',
            name='sub',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='marksheet',
            name='student',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
