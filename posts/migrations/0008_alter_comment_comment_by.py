# Generated by Django 4.0.2 on 2022-03-26 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_alter_schoolprofile_phone_number_and_more'),
        ('posts', '0007_remove_comment_responsed_by_alter_comment_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.studentprofile'),
        ),
    ]
