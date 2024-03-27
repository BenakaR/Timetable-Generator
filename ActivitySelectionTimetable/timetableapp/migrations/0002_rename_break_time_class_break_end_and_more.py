# Generated by Django 5.0 on 2024-03-04 15:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='class',
            old_name='break_time',
            new_name='break_end',
        ),
        migrations.RenameField(
            model_name='class',
            old_name='break_time_2',
            new_name='break_end_2',
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('user', 'course_id')},
        ),
    ]