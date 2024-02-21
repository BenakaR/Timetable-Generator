
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='selection'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.Logout, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('add-class/', views.ClassView, name='add-class'),
    path('add-classcourse/', views.ClassCourseView, name='add-classcourse'),
    path('add-course/', views.CourseView, name='add-course'),
    path('add-professor/', views.ProfessorView, name='add-professor'),
    path('update-course/<str:pk>/', views.updateCourseView, name='update-course'),
    path('update-professor/<str:pk>/', views.updateProfessorView, name='update-professor'),
    path('update-class/<str:pk>/', views.updateClassView, name='update-classview'),
    path('delete-course/<str:pk>/', views.deleteCourse, name='delete-course'),
    path('course_view/', views.CourseTable, name='course_view'),
    path('professor_view/', views.ProfessorTable, name='professor_view'),
    path('delete-professor/<str:pk>/', views.deleteProfessor, name='delete-professor'),
    path('class-view/', views.ClassTable, name='class_view'),
    path('delete-class/<str:pk>/', views.deleteClass, name='delete-class'),
    path('generate-timetable/<str:id>/', views.GenerateTimeTable, name='generate-timetable'),
    path('timetable/<str:id>/', views.TimeTableView, name='timetable'),
    path('activity/<str:pk>/', views.AddActivity, name='add-activity')
############    path('timetable/', views.TimeTable, name='timetable'), #############
]
