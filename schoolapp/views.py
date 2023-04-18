from django.shortcuts import render, redirect
from datetime import date
from schoolapp.EmailBackEnd import EmailBackEnd
from .models import *
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


#================= log-in /log-out views =============================
def Login(request):
    if request.method=="POST":
        user= EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))

        if user!=None:
            login(request, user)
            user_type= user.user_type
            if user_type =="1":
                return HttpResponseRedirect('admin_dashboard')
            elif user_type =="2":
                return HttpResponseRedirect('teacher_dashboard')
            elif user_type =="3":
                return HttpResponseRedirect('student_dashboard')
            else:
                return redirect('login')
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")
    else:
        return render(request, 'login_page.html')

def LogoutUser(request):
    logout(request)
    return HttpResponseRedirect("/")

#@login_required(login_url='/')

#================= Admin Views ===================================================    
def test(request):
    return render(request,'test.html')

def AdminDashboard(request):
    student = Student.objects.all()
    teacher = Teacher.objects.all()
    classs = Class.objects.all()

    student=student.count()
    teacher=teacher.count()
    classs=classs.count()

    return render(request,'admin/dashboard.html',locals())

#Student
def AddStudent(request):
    clas = Class.objects.all()
    section = Section.objects.all()
    session_year = Session_Year.objects.all()

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        dob= request.POST.get('dob')
        contact= request.POST.get('contact')
        profile_pic = request.FILES.get('profile_pic')

        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
       
        roll_no = request.POST.get('roll_no')

        address = request.POST.get('address')
        g_name = request.POST.get('g_name')
        g_contact= request.POST.get('g_contact')
        print("profile pic is :",profile_pic)

        if CustomUser.objects.filter(email=email).exists(): #server side validation for email== unique email id
           messages.error(request,'Email Is Already Taken, please rovide unique email Id !')
           return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists(): #server side validation for username== unique username 
           messages.error(request,'Username Is Already Taken, please rovide unique username !')
           return redirect('add_student')
        else:
            #save record in customuser table
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                user_type = 3
            )
            user.set_password(password)
            user.save()

            #save record in student table
            #cls = Class.objects.get(id=class_id)
            #session_year = Session_Year.objects.get(id=session_year_id)
           # section= Section.objects.get(id=section_id)

            student = Student(
                admin = user,
                gender = gender,
                dob= dob,
                roll_no= roll_no,
                contact= contact,
                address = address,
                guardian_name= g_name,
                guardian_contact =g_contact,
            )
            student.save()
            messages.success(request, user.first_name + "  " + user.last_name + "  Added Successfully !")
            return redirect('list_student')

    context = {
        'class':clas,
        'session_year':session_year,
        'section':section,
        
    }

    return render(request,'admin/student/add_student.html',context)

def EditStudent(request,student_id):
    print("id of teacher :" ,student_id)
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        dob= request.POST.get('dob')
        contact= request.POST.get('contact')
        profile_pic = request.FILES.get('profile_pic')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        roll_no = request.POST.get('roll_no')
        address = request.POST.get('address')
        g_name = request.POST.get('g_name')
        g_contact= request.POST.get('g_contact')
        
        #update customuser table data
        user = CustomUser.objects.get(id =student_id)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()

        #update Student table data
        student = Student.objects.get(admin_id = student_id)
        student.address = address
        student.gender = gender
        student.contact= contact
        student.roll_no= roll_no
        student.dob= dob
        student.guardian_name= g_name
        student.guardian_contact =g_contact

        student.save()
        messages.success(request,'Record Updated Successfully  !')
        return redirect('list_student')
    else:
        clas = Class.objects.all()
        section = Section.objects.all()
        session_year = Session_Year.objects.all()
        student=Student.objects.filter(admin_id=student_id)
        print("student details :",student)
    return render(request,'admin/student/edit_student.html',locals())

def DeleteStudent(request,student_id):
    student=CustomUser.objects.get(id=student_id)
    student.delete()
    messages.success(request, " Student deleted Successfully !")

    return redirect('list_student')

def ListStudent(request):
    student = Student.objects.all()
    return render(request,'admin/student/list_student.html',locals())

#Teacher 
def AddTeacher(request):
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        dob= request.POST.get('dob')
        phone= request.POST.get('phone_number')
        doj= request.POST.get('joining_date')
        qualification= request.POST.get('qualification')
        exp= request.POST.get('experience')
        profile_pic = request.FILES.get('profile_pic')

        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
       
        address = request.POST.get('address')
        
        if CustomUser.objects.filter(email=email).exists(): #server side validation for email== unique email id
           messages.error(request,'Email Is Already Taken, please rovide unique email Id !')
           return redirect('add_teacher')
        if CustomUser.objects.filter(username=username).exists(): #server side validation for username== unique username 
           messages.error(request,'Username Is Already Taken, please rovide unique username !')
           return redirect('add_teacher')
        else:
            #save record in customuser table
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                user_type = 2
            )
            user.set_password(password)
            user.save()

            #save record in student table
            teacher = Teacher(
                admin = user,
                gender = gender,
                dob= dob,
                doj= doj,
                qualification= qualification,
                phone= phone,
                address = address,
                experience= exp,
                
            )
            teacher.save()
            messages.success(request, user.first_name + "  " + user.last_name + "  Added Successfully !")
        return redirect('list_teacher')
    return render(request,'admin/teacher/add_teacher.html')

def EditTeacher(request,teacher_id):
    print("id of teacher :" ,teacher_id)    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        dob= request.POST.get('dob')
        phone= request.POST.get('phone_number')
        doj= request.POST.get('joining_date')
        qualification= request.POST.get('qualification')
        exp= request.POST.get('experience')
        profile_pic = request.FILES.get('profile_pic')

        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
       
        address = request.POST.get('address')

        user = CustomUser.objects.get(id = teacher_id)
        #upadate Customuser table
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()

        #upadate teacher table
        teacher = Teacher.objects.get(admin_id = teacher_id)
        teacher.address = address
        teacher.dob= dob
        teacher.doj= doj
        teacher.gender = gender
        teacher.qualification= qualification
        teacher.phone= phone
        teacher.experience= exp
    
        teacher.save()
        messages.success(request,'Record Updated Successfully  !')
        return redirect('list_teacher')
    else:
        teacher=Teacher.objects.filter(admin_id=teacher_id)
        print("teacher details :",teacher)
    return render(request,'admin/teacher/edit_teacher.html',locals())

def DeleteTeacher(request,teacher_id):
    print("Teacher Id:",teacher_id)
    teacher=CustomUser.objects.get(id=teacher_id)
    teacher.delete()
    messages.success(request, " Teacher deleted Successfully !")
    return redirect('list_teacher')

def ListTeacher(request):
    teacher = Teacher.objects.all()
    return render(request,'admin/teacher/list_teacher.html',locals())

#class
def AddClass(request):
    if request.method == "POST":
        class_name = request.POST.get('class')

        cls=Class(
            name=class_name,
        )
        cls.save()
        messages.success(request, " Class Added Successfully !")
        return redirect('list_class')
    return render(request,'admin/class/add_class.html')

def EditClass(request,class_id):
    if request.method == "POST":
        class_name = request.POST.get('class')

        classs=Class.objects.get(id=class_id)
        classs.name=class_name
        
        classs.save()
        messages.success(request,'Record Updated Successfully  !')
        return redirect('list_class')
    else:
        classs=Class.objects.get(id=class_id)
        
    return render(request,'admin/class/edit_class.html',locals())

def DeleteClass(request,class_id):
    classs= Class.objects.get(id=class_id)
    classs.delete()
    messages.success(request, " Class deleted Successfully !")
    return redirect('list_class')

def ListClass(request):
    classs = Class.objects.all()
    return render(request,'admin/class/list_class.html',locals())

#subject
def AddSubject(request):
    if request.method == "POST":
        subject_name = request.POST.get('name')
        classs = request.POST.get('class')
        teacher = request.POST.get('teacher')
        
        subject=Subject(
            name=  subject_name,
            classs_id= classs,
            teacher_id= teacher,
        )

        subject.save()
        messages.success(request, " Subject  Added Successfully !")
        return redirect('list_subject')
    else:
         classs=Class.objects.all()
         teacher=Teacher.objects.all()
    return render(request,'admin/subject/add_subject.html',locals())

def EditSubject(request,subject_id):
    if request.method == "POST":
        subject_name = request.POST.get('name')
        classs = request.POST.get('class')
        teacher = request.POST.get('teacher')

        subject=Subject.objects.get(id=subject_id)
        subject.name=subject_name
        subject.classs_id= classs
        subject.teacher_id= teacher

        subject.save()
        messages.success(request,'Record Updated Successfully  !')
        return redirect('list_subject')
    else:
        subject=Subject.objects.filter(id=subject_id)
        classs=Class.objects.all()
        teacher=Teacher.objects.all()
    return render(request,'admin/subject/edit_subject.html',locals())

def DeleteSubject(request,subject_id):
    subject= Subject.objects.get(id=subject_id)
    subject.delete()
    messages.success(request, " Subject deleted Successfully !")
    return redirect('list_subject')

def ListSubject(request):
    subject=Subject.objects.all()
    return render(request,'admin/subject/list_subject.html',locals())

#Timetable
def AddTimetable(request):
    return render(request,'admin/timetable/add_timetable.html')
def EditTimetable(request):
    return render(request,'admin/timetable/edit_timetable.html')
def DeleteTimetable(request):
    return render(request,'admin/timetable/delete_timetable.html')
def ListTimetable(request):
    return render(request,'admin/timetable/list_timetable.html')

#holiday
def AddHoliday(request):
    if request.method == "POST":
        holiday_name = request.POST.get('h_name')
        holiday_type= request.POST.get('h_type')
        start_date = request.POST.get('s_date')
        end_date = request.POST.get('e_date')
        
        if Holiday.objects.filter(holiday_name=holiday_name).exists():
           messages.error(request,'Holiday Is Already in the list !')
           return redirect('list_holiday')
        else:
            holiday= Holiday(
                holiday_name=holiday_name,
                holiday_type=holiday_type,
                start_date=start_date,
                end_date=end_date,
            )
            holiday.save()
            messages.success(request,  " Holiday Added Successfully !")
            return redirect('list_holiday')
    return render(request,'admin/holiday/add_holiday.html')

def EditHoliday(request,holiday_id):
    if request.method == "POST":
        holiday_name = request.POST.get('h_name')
        holiday_type= request.POST.get('h_type')
        start_date = request.POST.get('s_date')
        end_date = request.POST.get('e_date')

        holiday=Holiday.objects.get(id=holiday_id)
        holiday.holiday_name= holiday_name
        holiday.holiday_type= holiday_type
        holiday.start_date = start_date
        holiday.end_date = end_date

        holiday.save()
        messages.success(request,'Record Updated Successfully  !')
        return redirect('list_class')
    else:
        holiday= Holiday.objects.get(id=holiday_id)
    return render(request,'admin/holiday/edit_holiday.html',locals())

def DeleteHoliday(request,holiday_id):
    holiday=Holiday.objects.get(id=holiday_id)
    holiday.delete()
    messages.success(request, " Holiday deleted Successfully !")
    return redirect('list_holiday')
    
def ListHoliday(request):
    holiday=Holiday.objects.all()
    return render(request,'admin/holiday/list_holiday.html',locals())


################  library  ###################
def AddLibrary(request):
    return render(request,'admin/library/add_books.html')
def EditLibrary(request):
    return render(request,'admin/library/edi_books.html')
def DeleteLibrary(request):
    return render(request,'admin/library/delete_library.html')
def ListLibrary(request):
    return render(request,'admin/library/list_books.html')

#Admin view Leave
def AdminViewTeacher(request):

    t_leave=Teacher_Leave.objects.all()
    return render(request,'admin/leave/view_teacher_leave.html',locals())

def AdminApproveTeacher(request,id):
    leave=Teacher_Leave.objects.get(id=id)
    leave.status= 1
    leave.save()
    
    return redirect('admin_view_teacher_leave')

def AdminDisapproveTeacher(request,id):
    leave=Teacher_Leave.objects.get(id=id)
    leave.status= 2
    leave.save()
    
    return redirect('admin_view_teacher_leave')

#================= Teacher Views =================================

def TeacherDashboard(request):
    return render(request,'teacher/teacher_dashboard.html')

# Attendance 
def TakeAttendance(request):
    teacher_id = Teacher.objects.get(admin=request.user.id)
    
    subject= Subject.objects.filter(teacher = teacher_id)
    session_year = Session_Year.objects.all()

    return render(request,'teacher/take_attendance.html',locals())


#exam
def AddExam(request):
    if request.method == "POST":
        ex_name = request.POST.get('ex_name')
        date = request.POST.get('date')
       
        exam=Exam(
            name= ex_name,
            date= date,
        )
        exam.save()
        messages.success(request, " Exam  Added Successfully !")
        return redirect('list_exam')
    else:
        subject=Subject.objects.all()
    return render(request,'admin/exam/add_exam.html',locals())

def EditExam(request,exam_id):
    if request.method == "POST":
        ex_name = request.POST.get('ex_name')
        subject = request.POST.get('subject')
        date = request.POST.get('date')

        exam=Exam.objects.get(id=exam_id)
        exam.name= ex_name
        exam.subject_id= subject
        exam.date= date

        exam.save()
        messages.success(request,'Record Updated Successfully  !')
        return redirect('list_class')
    else:
        exam= Exam.objects.filter(id=exam_id)
        subject=Subject.objects.all()
    return render(request,'admin/exam/edit_exam.html',locals())


def DeleteExam(request,exam_id):
    exam=Exam.objects.get(id=exam_id)
    exam.delete()
    messages.success(request, " Exam deleted Successfully !")
    return redirect('list_exam')

def ListExam(request):
    exam=Exam.objects.all()
    return render(request,'admin/exam/list_exams.html',locals())

# Result  

def AddResult(request):
    if request.method == "POST":
        student= request.POST.get('student')
        exam = request.POST.get('exam')
        T_marks = request.POST.get('T_mark')
        O_marks = request.POST.get('O_mark')
       
        result=Result(
            student_id= student,
            exam_id= exam,
            Total_marks= T_marks,
            marks=O_marks,
        )
        result.save()
        messages.success(request, " Result Added Successfully !")
        return redirect('list_result')
    else:
        student=Student.objects.all()
        exam=Exam.objects.all()
    return render(request,'admin/result/add_result.html',locals())

def EditResult(request,result_id):
    if request.method == "POST":
        student= request.POST.get('student')
        exam = request.POST.get('exam')
        T_marks = request.POST.get('T_mark')
        O_marks = request.POST.get('O_mark')

        result=Result.objects.get(id=result_id)
        result.student_id= student
        result.exam_id= exam
        result.Total_marks= T_marks
        result.marks=O_marks

        result.save()
        messages.success(request,'Result Updated Successfully  !')
        return redirect('list_result')
    else:
        result= Result.objects.filter(id=result_id)
        student=Student.objects.all(id=result_id)
        exam=Exam.objects.all()
    return render(request,'admin/result/edit_result.html',locals())

def DeleteResult(request,result_id):
    result=Result.objects.get(id=result_id)
    result.delete()
    messages.success(request, "Result deleted Successfully !")
    return redirect('list_result')

def ListResult(request):
    results=Result.objects.all()
    return render(request,'admin/result/list_result.html',locals())

def TeacherLeave(request):
    if request.method == "POST":
        type= request.POST.get('type')
        days = request.POST.get('days')
        details = request.POST.get('details')
        sdate = request.POST.get('sdate')
        edate = request.POST.get('edate')
        t_id= Teacher.objects.get(admin_id=request.user.id)
        id =t_id.id
        print(type,days,details,sdate,edate,t_id,id)
        leave=Teacher_Leave(
            teacher_id= id,
            leave_type= type,
            No_of_days= days,
            details= details,
            start_date= sdate,
            end_date= edate,
        )
        leave.save()
        messages.success(request, "Leave Added Successfully !")
        return redirect('teacher_apply_leave')
    return render(request,'teacher/leave/apply_leave.html',locals())

def TeacherViewLeave(request):
    teacher= Teacher.objects.filter(admin=request.user.id)
    for i in teacher:
	    teacher_id=i.id

    teacher_leave_history = Teacher_Leave.objects.filter(teacher_id=teacher_id)
    return render(request,'teacher/leave/view_leave_history.html',locals())

 

#================= Student Views =================================
def StudentDashboard(request):
    return render(request,'student/student_dashboard.html')

#================= Other Views =================================
def UserProfile(request):
    
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        #email = request.POST.get('email')
        #username = request.POST.get('username')
        password = request.POST.get('password')
        print(profile_pic)
        
        customuser = CustomUser.objects.get(id = request.user.id)

        customuser.first_name = first_name
        customuser.last_name = last_name

        if password !=None and password != "":
            customuser.set_password(password)
        if profile_pic !=None and profile_pic != "":
            customuser.profile_pic = profile_pic
            
        customuser.save()
        messages.success(request,'Your Profile Updated Successfully !')
        return redirect('user_profile')
        
    else:
        user = CustomUser.objects.get(id = request.user.id)

    return render(request,'profile.html',locals())

#================= Send mails=================================
def SendMail(request):

    send_mail(
        "Testing mail functionality",
        "This is pravas sending mail from space !!!",
        "etnsolution2023@gmail.com",
        ["pravaspatra10@gmail.com"],
        fail_silently=False,
    )
    