# Generated by Django 4.0.2 on 2022-03-03 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_material', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studymaterial',
            name='link',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
    ]
