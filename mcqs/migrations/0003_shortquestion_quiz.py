# Generated by Django 3.2.11 on 2022-02-11 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mcqs', '0002_auto_20220210_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortquestion',
            name='quiz',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mcqs.quiz'),
            preserve_default=False,
        ),
    ]
