# Generated by Django 5.0 on 2024-03-03 14:51

import django.db.models.deletion
import multiselectfield.db.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_id', models.CharField(max_length=2000)),
                ('class_name', models.CharField(max_length=2000)),
                ('week_day', multiselectfield.db.fields.MultiSelectField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')], max_length=2000)),
                ('no_sessions', models.PositiveIntegerField(default=8)),
                ('class_mins', models.PositiveIntegerField(default=60)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('break_start', models.TimeField(blank=True, null=True)),
                ('break_start_2', models.TimeField(blank=True, null=True)),
                ('break_time', models.TimeField(blank=True, null=True)),
                ('break_time_2', models.TimeField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=1000)),
                ('course_name', models.CharField(max_length=1000)),
                ('course_type', models.CharField(choices=[('Theory', 'Theory'), ('Lab', 'Lab')], max_length=200)),
                ('credit_hours', models.PositiveIntegerField()),
                ('contact_hours', models.PositiveIntegerField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('professor_id', models.CharField(max_length=2000, primary_key=True, serialize=False)),
                ('professor_name', models.CharField(max_length=2000)),
                ('working_hours', models.IntegerField(default=100, null=True)),
                ('available_hours', models.IntegerField(default=100, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ClassCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetableapp.class')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetableapp.course')),
                ('professor_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='timetableapp.professor')),
            ],
            options={
                'unique_together': {('user', 'class_id', 'course_id')},
            },
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_id', models.CharField(max_length=2000)),
                ('activity_type', models.CharField(choices=[('Fixed', 'Fixed'), ('Replaceable', 'Replaceable')], max_length=2000)),
                ('class_id', models.CharField(max_length=200)),
                ('professor_id', models.CharField(max_length=200)),
                ('course_type', models.CharField(max_length=200)),
                ('day', models.CharField(max_length=2000)),
                ('start_time', models.PositiveIntegerField()),
                ('end_time', models.PositiveIntegerField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetableapp.classcourse')),
            ],
            options={
                'unique_together': {('user', 'activity_id')},
            },
        ),
    ]
