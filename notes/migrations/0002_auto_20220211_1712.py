# Generated by Django 3.2.11 on 2022-02-11 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('grade_and_subject', '0004_alter_grade_grade_name'),
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notes',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='notes',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='notes',
            name='grade',
            field=models.CharField(choices=[('NUR', 'Nursery'), ('LKG', 'L.K.G'), ('UKG', 'U.K.G'), ('1', 'One(1)'), ('2', 'Two(2)'), ('3', 'Three(3)'), ('4', 'Four(4)'), ('5', 'Five(5)'), ('6', 'Six(6)'), ('7', 'Seven(7)'), ('8', 'Eight(8)'), ('9', 'Nine(9)'), ('10', 'Ten(10)'), ('11', 'Eleven(11)'), ('12', 'Twelve(12)')], default='One', max_length=10),
        ),
        migrations.AlterField(
            model_name='notes',
            name='sub',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='grade_and_subject.subjects'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teacher_note', to='authentication.teacherprofile'),
        ),
    ]