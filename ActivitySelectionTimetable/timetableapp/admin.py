from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *

admin.site.site_header = "TimeTable Generator Administration"
admin.site.site_title = "TimeTable Admin"
admin.site.index_title = "Admin Page"

class ClassCourseDisp(admin.ModelAdmin):
    search_fields = ('class_id','professor_id','course_id')
    list_display = ('class_id','professor_id','course_id')
    list_editable = ('professor_id','course_id')

class SectionDisp(admin.ModelAdmin):
    search_fields = ('class_id','classroom_id')
    list_display = ('class_id','classroom_id')
    list_editable = ('classroom_id',)

admin.site.unregister(Group)

admin.site.register(Course)
admin.site.register(Professor)
admin.site.register(Class)
admin.site.register(ClassCourse,ClassCourseDisp)
admin.site.register(Activity)
