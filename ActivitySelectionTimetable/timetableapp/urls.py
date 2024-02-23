
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='selection'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.Logout, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('add-course/', views.CourseView, name='add-course'),
    path('course_view/', views.CourseTable, name='course_view'),
    path('update-course/<str:pk>/', views.updateCourseView, name='update-course'),
    path('delete-course/<str:pk>/', views.deleteCourse, name='delete-course'),

    path('add-professor/', views.ProfessorView, name='add-professor'),
    path('professor_view/', views.ProfessorTable, name='professor_view'),
    path('update-professor/<str:pk>/', views.updateProfessorView, name='update-professor'),
    path('delete-professor/<str:pk>/', views.deleteProfessor, name='delete-professor'),

    path('add-class/', views.ClassView, name='add-class'),
    path('class-view/', views.ClassTable, name='class_view'),
    path('update-class/<str:pk>/', views.updateClassView, name='update-classview'),
    path('delete-class/<str:pk>/', views.deleteClass, name='delete-class'),

    path('add-classcourse/', views.ClassCourseView, name='add-classcourse'),
    path('classcourse/', views.ClassCourseTable, name='view-classcourse'),
    path('update-classcourse/<str:pk>/', views.updateClassCourse, name='update-classcourse'),
    path('delete-classcourse/<str:pk>/', views.deleteClassCourse, name='delete-classcourse'),

    path('generate-timetable/<str:id>/', views.GenerateTimeTable, name='generate-timetable'),
    path('timetable/<str:id>/', views.TimeTableView, name='timetable'),
    path('activity/<str:pk>/', views.AddActivity, name='add-activity')
############    path('timetable/', views.TimeTable, name='timetable'), #############
]
