# Generated by Django 3.0.8 on 2020-08-14 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0002_auto_20200814_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='class_id',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='classroom_id',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='course_id',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='professor_id',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
