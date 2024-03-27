
from random import randint,choice

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from datetime import timedelta,datetime
from django.db import IntegrityError

errors = {}

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
                context['message'] = 'Username or Password is Incorrect.'
        
        return render(request, 'timetableapp/login.html', context)


def Logout(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('selection')
    else:
        form = CreateUserForm()
        context = {}
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'Account created successfully for ' + user)
                context['success'] = 'Account created successfully for ' + user

                return redirect('login')    
        context = {'form':form}
        return render(request, 'timetableapp/register.html', context)

@login_required(login_url='login')
def home(request):
    return render(request, 'timetableapp/home.html')


@login_required(login_url='login')
def CourseView(request):
    course = CourseForm()
    context = {'course': course}
    
    if request.method == 'POST' :
        course = CourseForm(request.POST)
        cors = course.save(commit = False)
        if course.is_valid():
            # messages.success(request, 'Course has been added successfully.')
            cors.user = request.user
            try:
                cors.save()
                context['success'] = 'Course has been added successfully.'
            except IntegrityError:
                context['message'] = 'Course already exists.'

        else:
            # messages.error(request, 'Course already exists or you have added wrong attributes.')
            context['message'] = 'Course already exists or you have added wrong attributes.'
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
        if course.is_valid() :
            cors = course.save(commit = False)
            if (cors.course_id == pk):
                cors.save()
                return redirect('/course_view')
            elif Course.objects.filter(user=request.user,course_id=form.course_id).count==0:
                cors.save()
                Course.objects.filter(user=request.user,course_id=pk).delete()
                return redirect('/course_view')
            else:
                context['message']="Course ID already exists"
        else:
            context['message']="Invalid details."
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
            context['success'] = 'Professor has been added successfully.'
            prof = professor.save(commit = False)
            prof.user = request.user
            prof.save()
        else:
            # messages.error(request, 'Professor already exists or you have added wrong attributes.')
            context['message'] = 'Professor ID already exists or you have added wrong attributes.'
    return render(request, 'timetableapp/AddProfessor.html', context)

@login_required(login_url='login')
def ProfessorTable(request):
    professor1 = Professor.objects.filter(user=request.user)
    context = {'professor1': professor1}
    return render(request, 'timetableapp/ProfessorTable.html', context)

@login_required(login_url='login')
def updateProfessorView(request, pk):
    prof = Professor.objects.get(user=request.user,professor_id=pk)
    form = ProfessorForm(instance=prof)
    context = {'form': form}
    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=prof)
        if form.is_valid():
            formsave = form.save(commit=False)
            if formsave.professor_id==pk :
                formsave.save()
                return redirect('professor_view')
            elif Professor.objects.filter(user=request.user,professor_id=formsave.professor_id).count()==0:
                formsave.save()
                Professor.objects.get(user=request.user,professor_id=pk).delete()
                return redirect('professor_view')
            else:
                context['message'] = 'Professor ID already exists'
        else:
            context['message'] = 'Invalid details.'

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
            try:
                sec.save()
                context['success'] = 'Class has been added.'
            except IntegrityError:
                context['message'] = 'Class ID already exists'
        else:
            # messages.error(request, 'Do not enter the same class ID')
            context['message'] = 'You have entered Wrong Attributes or haven\'t selected the Days'
    return render(request, 'timetableapp/AddClass.html', context)

@login_required(login_url='login')
def ClassTable(request):
    global errors
    sections = Class.objects.filter(user=request.user)
    context = {'sections': sections}
    context.update(errors)
    errors = {}
    return render(request, 'timetableapp/ClassTable.html', context)

@login_required(login_url='login')
def updateClassView(request, pk):
    section = Class.objects.get(user=request.user,class_id=pk)
    form = ClassForm(instance=section)
    context = {'form': form}
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=section)
        if form.is_valid():
            formsave = form.save(commit=False)
            if formsave.class_id==pk:
                formsave.save()
                return redirect('class_view')
            else:
                context['message'] = 'Class ID already exists'
        else:
            context['message'] = 'You have entered Wrong Attributes or haven\'t selected the Days'
    return render(request, 'timetableapp/ViewClass.html', context)
    

@login_required(login_url='login')
def deleteClass(request, pk):
    deleteClass = Class.objects.get(user=request.user,class_id=pk)
    context = {'delete': deleteClass}
    if request.method == 'POST':
        deleteActivities(request.user,pk)
        ClassCourse.objects.filter(user=request.user,class_id=deleteClass).delete()
        deleteClass.delete()
        return redirect('class_view')
    return render(request, 'timetableapp/deleteClass.html', context)


@login_required(login_url='login')
def ClassCourseView(request):
    sectioncourse = ClassCourseForm(request.user)
    sectioncourses = ClassCourse.objects.filter(user=request.user)
    context = {'sectioncourse': sectioncourse, 'sectioncourses': sectioncourses}
    if request.method == 'POST':
        sectioncourse = ClassCourseForm(request.user,request.POST)
        if sectioncourse.is_valid():
            try:
                sectioncourse.save()
                context['success'] = 'Course added for class.'
            except IntegrityError:
                context['message'] = 'Can not add duplicate course for class. Check for existing records.'
            except:
                context['message'] = 'ERROR'
    return render(request, 'timetableapp/AddClassCourse.html', context)

@login_required(login_url='login')
def ClassCourseTable(request):
    AssignList= ClassCourse.objects.filter(user=request.user)
    context = {'AssignList': AssignList}
    return render(request, 'timetableapp/ClassCourseTable.html', context)

@login_required(login_url='login')
def updateClassCourse(request, pk):
    assign = ClassCourse.objects.get(user=request.user,id=pk)
    sectioncourse = ClassCourseForm(request.user,instance=assign)
    context = {'sectioncourse': sectioncourse}
    if request.method == 'POST':
        sectioncourse = ClassCourseForm(request.user,request.POST, instance=assign)
        if sectioncourse.is_valid():
            try:
                sectioncourse.save()
                return redirect('/classcourse')
            except IntegrityError:
                context['message'] = 'Can not add duplicate course for class. Check for existing records.'
            except:
                context['message'] = 'ERROR'
    return render(request, 'timetableapp/AddClassCourse.html', context)

@login_required(login_url='login')
def deleteClassCourse(request, pk):
    deleteAssign = ClassCourse.objects.get(user=request.user,id=pk)
    context = {'delete': deleteAssign}
    if request.method == 'POST':
        ClassCourse.objects.filter(user=request.user,id=pk).delete()
        deleteAssign.delete()
        return redirect('view-classcourse')
    return render(request, 'timetableapp/deleteClassCourse.html', context)


@login_required(login_url='login')
def GenerateTimeTable(request, id):
    currentUser = request.user
    try:
        section = Class.objects.get(user=currentUser,class_id=id)
        sectioncourses = list(ClassCourse.objects.filter(user=currentUser,class_id=section))
    except Class.DoesNotExist:
        messages.error(request, 'Class does not exist')
        return redirect('class_view')

    if len(sectioncourses) <= 0:
        messages.error(request, 'Courses does not exist.')
        return redirect('class_view')

    if Activity.objects.filter(user=currentUser,activity_type='Replaceable',class_id=id).count() != 0:
        deleteActivities(currentUser,id,"Theory")
        deleteActivities(currentUser,id,"Lab")
    totalDays = len(section.week_day)
    sessionlist, breaktime = timeCalculate(currentUser,id)
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
            course: Course = Course.objects.get(user=currentUser,course_type = 'Lab',
                                                course_id=sectioncourses[k].course_id.course_id)
        except Course.DoesNotExist:
            # messages.error(request, 'Lab Course not found')
            continue

        try:
            professor = Professor.objects.get(professor_id=sectioncourses[k].professor_id.professor_id)
        except Professor.DoesNotExist:
            # messages.error(request, 'Professor not found')
            continue

        courseCount = Activity.objects.filter(user=currentUser,course=sectioncourses[k]).count()
        courseLecs = course.credit_hours - courseCount
        lecDuration = course.contact_hours / course.credit_hours
        j = 0
        while j < courseLecs:
            lecFlag = True
            if DupNum > workingHours + 5:
                deleteActivities(currentUser,id,'Lab')
                # messages.error(request, 'Solution does not exist.')
                errors['message'] = 'Solution does not exist.'
                DupNum +=1
                break

            if DupNum < 5:
                lecDay = randint(0, totalDays - 1)
                lecStartTime = choice(breaktime)
                # while lecStartTime in breaktime:
                #     lecStartTime = random.randint(0,lenSessList)
                if lecStartTime + lecDuration > lenSessList:
                    lecFlag = False
            else:
                lecStartTime += 1
                if lecStartTime + lecDuration > lenSessList:
                    lecDay = (lecDay + 1) % totalDays
                    lecStartTime = 0

            if lecFlag and (lecStartTime < lenSessList):
                activityFlag = True
                activityID = [section.week_day[lecDay]] * int(lecDuration)
                for i in range(int(lecDuration)):
                    activityID[i] += '-' + str(lecStartTime + i) + '-' + str(section.class_id)
                    if Activity.objects.filter(user=currentUser,
                                            day=section.week_day[lecDay],
                                            start_time=lecStartTime + i,
                                            class_id=section.class_id).count() != 0 or \
                            Activity.objects.filter(user=currentUser,
                                                day=section.week_day[lecDay],
                                                start_time=lecStartTime + i,
                                                professor_id=professor.professor_id).count() != 0 :
                        activityFlag = False
                        DupNum += 1
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

    DupNum = 0
    lecDay = 0
    lecStartTime = 0
    for k in range(0, len(sectioncourses)):
        if DupNum > (workingHours + 5):
            break

        try:
            course: Course = Course.objects.get(user=currentUser,
                                                course_id=sectioncourses[k].course_id.course_id,
                                                course_type = 'Theory')
        except Course.DoesNotExist:
            # messages.error(request, 'Course not found')
            continue

        try:
            professor = Professor.objects.get(user=currentUser,
                                              professor_id=sectioncourses[k].professor_id.professor_id)
        except Professor.DoesNotExist:
            # messages.error(request, 'Professor not found')
            continue

        courseCount = Activity.objects.filter(user=currentUser,course=sectioncourses[k]).count()
        courseLecs = course.credit_hours - courseCount
        lecDuration = course.contact_hours / course.credit_hours
        j = 0
        DupNum = 0
        lecDay = 0
        while j < courseLecs:
            lecFlag = True
            
            if DupNum > workingHours + 20:
                deleteActivities(currentUser,id,'Theory')
                # messages.error(request, 'Solution does not exist.')
                errors['message'] = 'Solution does not exist.'
                DupNum +=1
                break

            if DupNum < 20:
                lecDay = randint(0, totalDays - 1)
                lecStartTime = randint(0,lenSessList)
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


            if lecFlag and (lecStartTime < lenSessList):
                activityFlag = True
                activityID = [section.week_day[lecDay]] * int(lecDuration)
                for i in range(int(lecDuration)):
                    activityID[i] += '-' + str(lecStartTime + i) + '-' + str(section.class_id)
                    if Activity.objects.filter(user=currentUser,
                                            day=section.week_day[lecDay],
                                            start_time=lecStartTime + i,
                                            class_id=section.class_id).count() != 0 or \
                            Activity.objects.filter(user=currentUser,
                                                day=section.week_day[lecDay],
                                                start_time=lecStartTime + i,
                                                professor_id=professor.professor_id).count() != 0 :
                        activityFlag = False
                        DupNum += 1
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

    # messages.success(request, 'Timetable generated')
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
    timelist = []
    breakPosition=[]
    st = datetime.combine(datetime.today(),section.start_time)
    end = datetime.combine(datetime.today(),section.end_time)
    min = section.class_mins
    count=0
    while st < end:
        if st.time()==section.break_start:
            s = str(st.time())[0:5]
            e = datetime.combine(datetime.today(),section.break_end)
            timelist.append( [str(st.time())[0:5] , str(e.time())[0:5]])
            st = e
            breakPosition.append(count)
        if st.time()==section.break_start_2:
            s = str(st.time())[0:5]
            e = datetime.combine(datetime.today(),section.break_end_2)
            timelist.append( [str(st.time())[0:5] , str(e.time())[0:5]])
            st = e
            breakPosition.append(count)
        s = str(st.time())[0:5]
        st = st + timedelta(minutes=min)
        s = s + ' - ' + str(st.time())[0:5]
        timelist.append(s)
        count += 1
    return timelist,breakPosition


@login_required(login_url='login')
def TimeTableView(request, id):
    try:
        section = Class.objects.get(user=request.user,class_id=id)
    except Class.DoesNotExist:
        # messages.error(request, 'Activity does not exist')
        return redirect('class_view')

    courses = Course.objects.filter(user=request.user)
    professors = Professor.objects.filter(user=request.user)
    activities = Activity.objects.filter(user=request.user,class_id=id)
    timelist,breakcounts = timeCalculate(request.user,id)
    breaklist=[]
    tmp=0
    for i in breakcounts:
        breaklist.append(timelist[i+tmp])
        tmp += 1
    activityform = ActivityForm(request.user)
    
    if request.method == 'POST':
        actform = ActivityForm(request.user, request.POST)
        if actform.is_valid():
            act = actform.save(commit=False)
            act.end_time = act.start_time
            act.start_time = act.start_time - 1
            act.day = act.day[2:-2]
            act.activity_id = act.day +'-'+ str(act.start_time) +'-'+ act.course.class_id.class_id
            Activity.objects.filter(user=request.user,activity_id=act.activity_id).delete()
            act.save()
        else:
            context['message'] = 'Error editing activity'
    context = {'section': section, 'courses': courses, 'professors':professors, 
                    'activities': activities, 'timings':timelist, 'timingss':range(section.no_sessions), 'breaks':breakcounts,
                    'breaklist':breaklist , 'totalLength':section.no_sessions+len(breakcounts),'activityform':activityform}
    return render(request, 'timetableapp/TimeTable.html', context)
    
    
@login_required(login_url='login')
def AddActivity(request, pk):
    activity = Activity.objects.get(user=request.user,activity_id=pk)
    section = Class.objects.get(user=request.user,class_id = activity.class_id)
    actform = ActivityFormUpdate(request.user,instance = activity)
    context = {'actform': actform, 'section':section}
    if request.method == 'POST':
        actform = ActivityFormUpdate(request.user,request.POST,instance=activity)
        if actform.is_valid():
            actform.save()
            return redirect('/timetable/'+ section.class_id)
        else:
            messages.error(request, 'Error editing activity')
    return render(request, 'timetableapp/AddActivity.html', context)
