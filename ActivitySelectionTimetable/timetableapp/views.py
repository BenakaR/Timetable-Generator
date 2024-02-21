
import random

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from datetime import timedelta,datetime

from .models import Course


def loginPage(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('selection')
    else:
        
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password= password )
            if user is not None:
                login(request, user)
                return redirect('selection')
            else:
                messages.info(request, 'Username or Password is Incorrect')
                return render(request, 'timetableapp/login.html', context)

        
        return render(request, 'timetableapp/login.html', context)


def Logout(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('selection')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'Account created successfully for ' + user)
                return redirect('login')

        context = {'form':form}
        return render(request, 'timetableapp/register.html', context)

@login_required(login_url='login')
def home(request):
    course = CourseForm()
    professor = ProfessorForm()
    section = ClassForm()
    sectioncourse = ClassCourseForm(request.user)
    activity = ActivityForm()
    context = {
                'course': course,'professor': professor,'section': section,
                'sectioncourse': sectioncourse, 'activity': activity
            }


    return render(request, 'timetableapp/home.html', context)


@login_required(login_url='login')
def CourseView(request):
    course = CourseForm()
    context = {'course': course}
    
    if request.method == 'POST':
        course = CourseForm(request.POST)
        if course.is_valid():
            # messages.success(request, 'Course has been added successfully.')
            cors = course.save(commit = False)
            cors.user = request.user
            cors.save()
        else:
            messages.error(request, 'Course already exists or you have added wrong attributes.')
    return render(request, 'timetableapp/AddCourse.html', context)


@login_required(login_url='login')
def CourseTable(request):
    course = Course.objects.filter(user=request.user)
    context = {'course': course}
    return render(request, 'timetableapp/CourseTable.html', context)

@login_required(login_url='login')
def updateCourseView(request, pk):
    form = Course.objects.get(user=request.user,course_id=pk)
    course = CourseForm(instance=form)
    context = {'course': course}
    if request.method == 'POST':
        course = CourseForm(request.POST, instance=form)
        if course.is_valid():
            course.save()
            return redirect('/course_view')
    return render(request, 'timetableapp/AddCourse.html', context)

@login_required(login_url='login')
def deleteCourse(request, pk):
    delete_course = Course.objects.get(user=request.user,course_id=pk)
    context = {'course_delete': delete_course}
    if request.method == 'POST':
        delete_course.delete()
        return redirect('/course_view')

    return render(request, 'timetableapp/delete.html', context)

@login_required(login_url='login')
def ProfessorView(request):
    professor = ProfessorForm()
    professor1 = Professor.objects.filter(user=request.user)

    context = {'professor': professor, 'professor1': professor1}
    if request.method == 'POST':
        professor = ProfessorForm(request.POST)
        if professor.is_valid():
            # messages.success(request, 'Professor has been added successfully.')
            prof = professor.save(commit = False)
            prof.user = request.user
            prof.save()
        else:
            messages.error(request, 'Professor already exists or you have added wrong attributes.')
    return render(request, 'timetableapp/AddProfessor.html', context)


@login_required(login_url='login')
def ProfessorTable(request):
    professor1 = Professor.objects.filter(user=request.user)
    context = {'professor1': professor1}
    return render(request, 'timetableapp/ProfessorTable.html', context)


@login_required(login_url='login')
def updateProfessorView(request, pk):
    professor = Professor.objects.get(user=request.user,professor_id=pk)
    form = ProfessorForm(instance=professor)
    context = {'form': form}
    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            return redirect('/add-professor')
    return render(request, 'timetableapp/ViewSection.html', context)

@login_required(login_url='login')
def deleteProfessor(request, pk):
    deleteprofessor = Professor.objects.get(user=request.user,professor_id=pk)
    context = {'delete': deleteprofessor}
    if request.method == 'POST':
        deleteprofessor.delete()
        return redirect('/professor_view')

    return render(request, 'timetableapp/deleteProfessor.html', context)


@login_required(login_url='login')
def ClassView(request):
    section = ClassForm()
    sections = Class.objects.filter(user=request.user)
    context = {'section': section, 'sections': sections}
    if request.method == 'POST':
        section = ClassForm(request.POST)
        if section.is_valid():  
            # messages.success(request, 'Class has been added.')
            sec = section.save(commit = False)
            sec.user = request.user
            sec.save()
            return redirect('/add-classcourse')    # add 
        else:
            messages.error(request, 'Do not enter the same class ID')
    return render(request, 'timetableapp/AddClass.html', context)

@login_required(login_url='login')
def ClassCourseView(request):
    sectioncourse = ClassCourseForm(request.user)
    sectioncourses = ClassCourse.objects.filter(user=request.user)

    context = {'sectioncourse': sectioncourse, 'sectioncourses': sectioncourses}
    if request.method == 'POST':
        sectioncourse = ClassCourseForm(request.user,request.POST)
        if sectioncourse.is_valid():
            messages.success(request, "Course added for class.")
            sectioncourse.save()
        else:
            messages.error(request, 'Can not add duplicate course for class.')
    return render(request, 'timetableapp/AddClassCourse.html', context)


@login_required(login_url='login')
def updateClassView(request, pk):
    section = Class.objects.get(user=request.user,class_id=pk)
    form = ClassForm(instance=section)
    context = {'form': form}
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect('/add-classcourse')
    return render(request, 'timetableapp/ViewClass.html', context)


@login_required(login_url='login')
def deleteClass(request, pk):
    deleteClass = Class.objects.get(user=request.user,class_id=pk)
    context = {'delete': deleteClass}
    if request.method == 'POST':
        deleteActivities(pk)
        deleteCLassCourses(request.user,pk)
        deleteClass.delete()

        return redirect('/class-view')

    return render(request, 'timetableapp/deleteClass.html', context)


def deleteCLassCourses(usr,id):
    ClassCourse.objects.filter(user=usr,class_id=id).delete()


@login_required(login_url='login')
def ClassTable(request):
    sections = Class.objects.filter(user=request.user)
    context = {'sections': sections}
    return render(request, 'timetableapp/ClassTable.html', context)


@login_required(login_url='login')
def TimeTable(request):
    sections = Class.objects.filter(user=request.user)
    context = {'sections': sections}
    return render(request, 'timetableapp/TimeTable.html', context)


@login_required(login_url='login')
def GenerateTimeTable(request, id):
    try:
        section = Class.objects.get(user=request.user,class_id=id)
        sectioncourses = list(ClassCourse.objects.filter(user=request.user,class_id=id))
    except Class.DoesNotExist:
        messages.error(request, 'Class does not exist')
    else:
        if len(sectioncourses) > 0:
            if Activity.objects.filter(user=request.user,activity_type='Replaceable',class_id=id).count() != 0:
                deleteActivities(request.user,id,"Theory")
                deleteActivities(request.user,id,"Lab")
            totalDays = len(section.week_day)
            sessionlist, breaktime = timeCalculate(request.user,id)
            lenSessList = len(sessionlist)-len(breaktime)
            breaktime = [0] + breaktime
            workingHours = totalDays * len(sessionlist)
            lecDay = 0
            lecStartTime = 0
            DupNum = 0
            for k in range(0, len(sectioncourses)):
                if DupNum > (workingHours + 5):
                    break
                try:
                    course: Course = Course.objects.get(user=request.user,course_id=sectioncourses[k].course_id_id,course_type = 'Lab')
                except Course.DoesNotExist:
                    pass#messages.error(request, 'Course not found')
                else:
                    try:
                        professor = Professor.objects.get(professor_id=sectioncourses[k].professor_id_id)
                    except Professor.DoesNotExist:
                        messages.error(request, 'Professor not found')
                    else:
                        courseCount = Activity.objects.filter(user=request.user,course=sectioncourses[k]).count()
                        courseLecs = course.credit_hours - courseCount
                        lecDuration = course.contact_hours / course.credit_hours
                        j = 0
                        while j < courseLecs:
                            lecFlag = True
                            if DupNum < workingHours + 5:
                                if DupNum < 5:
                                    lecDay = random.randint(0, totalDays - 1)
                                    lecStartTime = random.choice(breaktime)
                                    # while lecStartTime in breaktime:
                                    #     lecStartTime = random.randint(0,lenSessList)
                                    if lecStartTime + lecDuration > lenSessList:
                                        lecFlag = False
                                else:
                                    lecStartTime += 1
                                    if lecStartTime + lecDuration > lenSessList:
                                        lecDay = (lecDay + 1) % totalDays
                                        lecStartTime = 0

                                if lecFlag:
                                    if lecStartTime < lenSessList:
                                        activityFlag = True
                                        activityID = [section.week_day[lecDay]] * int(lecDuration)
                                        for i in range(int(lecDuration)):
                                            activityID[i] += '-' + str(lecStartTime + i) + '-' + str(section.class_id)
                                            # for activity in activities:
                                            if Activity.objects.filter(user=request.user,
                                                                    day=section.week_day[lecDay],
                                                                    start_time=lecStartTime + i,
                                                                    class_id=section.class_id).count() != 0 or \
                                                    Activity.objects.filter(user=request.user,
                                                                        day=section.week_day[lecDay],
                                                                        start_time=lecStartTime + i,
                                                                        professor_id=professor.professor_id).count() != 0 :
                                                activityFlag = False
                                                DupNum += 1
                                            # break
                                        if activityFlag:
                                            for i in range(int(lecDuration)):
                                                newActivity = Activity(activity_id=activityID[i],
                                                                    activity_type='Replaceable',
                                                                    course=sectioncourses[k],
                                                                    day=section.week_day[lecDay],
                                                                    start_time=lecStartTime + i,
                                                                    end_time=lecStartTime + i + 1)
                                                newActivity.save()
                                                professor.available_hours = professor.available_hours - 1
                                                professor.save()
                                            DupNum = 0
                                            j += 1

                            else:
                                #Activity.objects.filter(class_id=section.class_id).delete()
                                deleteActivities(request.user,id,'Lab')
                                messages.error(request, 'Solution does not exist.')
                                DupNum +=1
            DupNum = 0
            lecDay = 0
            lecStartTime = 0
            for k in range(0, len(sectioncourses)):
                if DupNum > (workingHours + 5):
                    break
                try:
                    course: Course = Course.objects.get(user=request.user,course_id=sectioncourses[k].course_id_id,course_type = 'Theory')
                except Course.DoesNotExist:
                    pass#messages.error(request, 'Course not found')
                else:
                    try:
                        professor = Professor.objects.get(user=request.user,professor_id=sectioncourses[k].professor_id_id)
                    except Professor.DoesNotExist:
                        messages.error(request, 'Professor not found')
                    else:
                        courseCount = Activity.objects.filter(user=request.user,course=sectioncourses[k]).count()
                        courseLecs = course.credit_hours - courseCount
                        lecDuration = course.contact_hours / course.credit_hours
                        j = 0
                        DupNum = 0
                        lecDay = 0
                        while j < courseLecs:
                            lecFlag = True
                            
                            if DupNum < workingHours + 20:
                                if DupNum < 20:
                                    lecDay = random.randint(0, totalDays - 1)
                                    lecStartTime = random.randint(0,lenSessList)
                                    # while lecStartTime in breaktime:
                                    #     lecStartTime = random.randint(0,lenSessList)
                                    if lecStartTime + lecDuration > lenSessList:
                                        lecFlag = False
                                elif DupNum == 20:
                                    lecDay = 0
                                else:
                                    lecStartTime += 1
                                    if lecStartTime + lecDuration > lenSessList:
                                        lecDay = (lecDay + 1) % totalDays
                                        lecStartTime = 0

                                if lecFlag:
                                    if lecStartTime < lenSessList:
                                        activityFlag = True
                                        activityID = [section.week_day[lecDay]] * int(lecDuration)
                                        for i in range(int(lecDuration)):
                                            activityID[i] += '-' + str(lecStartTime + i) + '-' + str(section.class_id)
                                            # for activity in activities:
                                            if Activity.objects.filter(user=request.user,
                                                                    day=section.week_day[lecDay],
                                                                    start_time=lecStartTime + i,
                                                                    class_id=section.class_id).count() != 0 or \
                                                    Activity.objects.filter(user=request.user,
                                                                        day=section.week_day[lecDay],
                                                                        start_time=lecStartTime + i,
                                                                        professor_id=professor.professor_id).count() != 0 :
                                                activityFlag = False
                                                DupNum += 1
                                            # break
                                        if activityFlag:
                                            for i in range(int(lecDuration)):
                                                newActivity = Activity(activity_id=activityID[i],
                                                                    activity_type='Replaceable',
                                                                    course=sectioncourses[k],
                                                                    day=section.week_day[lecDay],
                                                                    start_time=lecStartTime + i,
                                                                    end_time=lecStartTime + i + 1)
                                                newActivity.save()
                                                professor.available_hours = professor.available_hours - 1
                                                professor.save()
                                            DupNum = 0
                                            j += 1

                            else:
                                #Activity.objects.filter(class_id=section.class_id).delete()
                                deleteActivities(request.user,id,'Theory')
                                messages.error(request, 'Solution does not exist.')
                                DupNum +=1
                                break
            
            messages.success(request, 'Timetable generated')
            #return redirect('timetable/')
        else:
            messages.error(request, 'Courses does not exist.')
    
    sections = Class.objects.filter(user=request.user)
    context = {'sections': sections}
    return redirect('class_view')



def deleteActivities(usr,id,type=None):
    if type == None:
        activities = list(Activity.objects.filter(user=usr,class_id=id,activity_type='Replaceable'))
    else:
        activities = list(Activity.objects.filter(user=usr,class_id=id,activity_type='Replaceable',course_type=type))
    for activity in activities:
        #course = Course.objects.get(course_id=activity.course_id)
        professor = Professor.objects.get(professor_id=activity.professor_id)
        professor.available_hours += 1
        professor.save()
    if type == None:
        Activity.objects.filter(user=usr,class_id=id,activity_type='Replaceable').delete()
    else:
        Activity.objects.filter(user=usr,class_id=id,activity_type='Replaceable',course_type=type).delete()


def timeCalculate(usr,id):
    section = Class.objects.get(user=usr,class_id=id)
    l = []
    st = datetime.combine(datetime.today(),section.start_time)
    end = datetime.combine(datetime.today(),section.end_time)
    min = section.class_mins
    count=0
    ll=[]
    while st < end:
        s = str(st.time())[0:5]
        if st.time()==section.break_start:
            e = datetime.combine(datetime.today(),section.break_time)
            l.append( [str(st.time())[0:5] , str(e.time())[0:5]])
            st = e
            s = str(st.time())[0:5]
            ll.append(count)
        if st.time()==section.break_start_2:
            e = datetime.combine(datetime.today(),section.break_time_2)
            l.append( [str(st.time())[0:5] , str(e.time())[0:5]])
            st = e
            s = str(st.time())[0:5]
            ll.append(count)
        st = st + timedelta(minutes=min)
        s = s + ' - ' + str(st.time())[0:5]
        l.append(s)
        count += 1
    return l,ll



@login_required(login_url='login')
def TimeTableView(request, id):
    try:
        section = Class.objects.get(user=request.user,class_id=id)
        courses = Course.objects.filter(user=request.user)
        professors = Professor.objects.filter(user=request.user)
        activities = Activity.objects.filter(user=request.user,class_id=id)
        l,ll = timeCalculate(request.user,id)
        breakss=[]
        c=0
        for i in ll:
            breakss.append(l[i+c])
            c += 1
        activityform = ActivityForm()
        context_1 = {'section': section, 'courses': courses, 'professors':professors, 
                     'activities': activities, 'timings':l, 'timingss':range(len(l)-len(ll)), 'breaks':ll,
                     'breakss':breakss , 'activityform':activityform}
        if request.method == 'POST':
            actform = ActivityForm(request.POST)
            if actform.is_valid():
                act = actform.save(commit=False)
                act.end_time = act.start_time
                act.start_time = act.start_time - 1
                act.day = act.day[2:-2]
                act.activity_id = act.day +'-'+ str(act.start_time) +'-'+ act.course.class_id.class_id
                Activity.objects.filter(user=request.user,activity_id=act.activity_id).delete()
                act.save()
            else:
                messages.error(request, 'Error editing activity')
        return render(request, 'timetableapp/TimeTable.html', context_1)
    except Class.DoesNotExist:
        messages.error(request, 'Activity does not exist')
    
        sections = Class.objects.filter(user=request.user)
        context_2 = {'sections': sections}
        return render(request, 'timetableapp/ClassTable.html', context_2)
    
@login_required(login_url='login')
def AddActivity(request, pk):
    activity = Activity.objects.get(user=request.user,activity_id=pk)
    section = Class.objects.get(user=request.user,class_id = activity.class_id)
    actform = ActivityFormUpdate(instance = activity)
    context = {'actform': actform, 'section':section}
    if request.method == 'POST':
        actform = ActivityFormUpdate(request.POST,instance=activity)
        if actform.is_valid():
            actform.save()
            return redirect('/timetable/'+ section.class_id)
        else:
            messages.error(request, 'Error editing activity')
    return render(request, 'timetableapp/AddActivity.html', context)
