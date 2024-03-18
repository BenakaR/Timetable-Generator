from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email', 'password1', 'password2']
        label = {
            'password1':'Password', 'password2':'Password'
        }
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['user','course_id', 'course_name', 'course_type', 'credit_hours', 'contact_hours']
        exclude = ['user']
        labels = {'credit_hours':'No of classes per week',
                  'contact_hours':'Total hours per week'}


class ProfessorForm(forms.ModelForm):
    
    class Meta:
        model = Professor
        fields = ['user','professor_id', 'professor_name', 'working_hours','available_hours']
        exclude = ['user']
        labels = {}

class TimeInput(forms.TimeInput):
    input_type = "time"

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['user','class_id','class_name','week_day','no_sessions','class_mins','start_time',
                    'end_time','break_start','break_end','break_start_2','break_end_2']
        exclude = ['user']
        labels = {
            # 'class_id':'Class ID',
            # 'class_name':'Class Name',
            'week_day':'Select the days when classes are conducted',
            'no_sessions':'Number of sessions per day',
            'class_mins':'Minutes per Session',
            'start_time':'Start of the Day',
            'end_time':'End of the Day',
            'break_start':'Short break start time',
            'break_end':'Short break end time',
            'break_start_2':'Long break start time',
            'break_end_2':'Long break end time',
        }
        widgets = {
            "start_time": TimeInput(),
            "end_time" : TimeInput(),
            "break_start": TimeInput(),
            "break_end": TimeInput(),
            "break_start_2": TimeInput(),
            "break_end_2": TimeInput(),
        }
        
class ClassCourseForm(forms.ModelForm):
    class Meta:
        model = ClassCourse
        fields = ['user','class_id','course_id','professor_id']
        exclude = ['user']

    def __init__(self, user, *args,  **kwargs):
        super(ClassCourseForm, self).__init__(*args, **kwargs)
        self.fields['class_id'].queryset = Class.objects.filter(user=user)
        self.fields['professor_id'].queryset = Professor.objects.filter(user=user)
        self.fields['course_id'].queryset = Course.objects.filter(user=user)

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [ 'activity_type', 'course', 'day',
                  'start_time']
        labels = {
            'start_time':'Session Number'
        }
    WEEK_DAY = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday')
    )
    day = forms.MultipleChoiceField(choices=WEEK_DAY)
    def __init__(self, *args,  **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].initial = 1

class ActivityFormUpdate(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['activity_type','course']
        labels = {
            'activity_type':'Should be Fixed During Generation?(Fixed/Replace) '
        }

