# Generated by Django 4.0.2 on 2022-03-03 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('researchs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchdetail',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='researchs.category'),
        ),
    ]