from django.contrib import admin
from .models import *

class ClassCourseDisp(admin.ModelAdmin):
    search_fields = ('class_id','professor_id','course_id')
    list_display = ('class_id','professor_id','course_id')
    list_editable = ('professor_id','course_id')

class SectionDisp(admin.ModelAdmin):
    search_fields = ('class_id','classroom_id')
    list_display = ('class_id','classroom_id')
    list_editable = ('classroom_id',)



admin.site.register(Course)
admin.site.register(Professor)
admin.site.register(Classroom)
admin.site.register(Class)
admin.site.register(ClassCourse,ClassCourseDisp)
admin.site.register(SectionClassroom,SectionDisp)
admin.site.register(Activity)

