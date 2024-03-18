from typing import Iterable
from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import time

class Course(models.Model):
    COURSE_TYPE = (
        ('Theory', 'Theory'),
        ('Lab', 'Lab')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    course_id = models.CharField(max_length=1000)
    course_name = models.CharField(max_length=1000)
    course_type = models.CharField(max_length=200, choices=COURSE_TYPE)
    credit_hours = models.PositiveIntegerField()
    contact_hours = models.PositiveIntegerField()
    class Meta:
        unique_together = ('user','course_id')

    def __str__(self):
        return self.course_id + ' - ' + self.course_name
    
    def save(self, *args, **kwargs):
        if self.course_id == '123':
            raise ValidationError('Cant put 123')
        return super().save(*args, **kwargs)

    

class Professor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    professor_id = models.CharField(max_length=2000,primary_key=True)
    professor_name = models.CharField(max_length=2000)
    working_hours = models.IntegerField(null=True,default=100)
    available_hours = models.IntegerField(null=True,default=100)
    def __str__(self):
        return self.professor_name
    

class Class(models.Model):
    WEEK_DAY = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    class_id = models.CharField(max_length=2000)
    class_name = models.CharField(max_length=2000)
    week_day = MultiSelectField(max_length=2000, choices=WEEK_DAY, max_choices=6)
    no_sessions = models.PositiveIntegerField(default = 8)
    class_mins = models.PositiveIntegerField(default = 60)
    start_time = models.TimeField(default=time(00,00))
    end_time = models.TimeField(default=time(00,00))
    break_start = models.TimeField(null=True,blank=True)
    break_start_2 = models.TimeField(null=True,blank=True)
    break_end = models.TimeField(null=True,blank=True)
    break_end_2 = models.TimeField(null=True,blank=True)
    class Meta:
        unique_together = ('user','class_id')

    def __str__(self):
        return self.class_id + ' - ' + self.class_name


# table to store courses for class
class ClassCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        unique_together = ('user','class_id', 'course_id')
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    professor_id = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True, blank=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self) :
        return self.course_id.course_id +' - '+ self.course_id.course_name +' - '+ self.professor_id.professor_name
    
    def save(self, *args, **kwargs):
        self.user = self.class_id.user
        super(ClassCourse, self).save(*args, **kwargs)


class Activity(models.Model):
    class Meta:
        unique_together = ('user','activity_id')
    ACTIVITY_TYPE = (
        ('Fixed', 'Fixed'),
        ('Replaceable', 'Replaceable')
    )
    WEEK_DAY = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    activity_id = models.CharField(max_length=2000)
    activity_type = models.CharField(max_length=2000, choices=ACTIVITY_TYPE)
    class_id = models.CharField(max_length=200)
    professor_id = models.CharField(max_length=200)
    course = models.ForeignKey(ClassCourse,on_delete=models.CASCADE)
    course_type = models.CharField(max_length=200)
    day = models.CharField(max_length=2000)
    start_time = models.PositiveIntegerField()
    end_time = models.PositiveIntegerField()

    def __str__(self):
        return self.activity_id

    def save(self, *args, **kwargs):
        self.user = self.course.user
        self.class_id = self.course.class_id.class_id
        self.professor_id = self.course.professor_id.professor_id
        self.course_type = self.course.course_id.course_type
        super(Activity, self).save(*args, **kwargs)
