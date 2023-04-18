from django.contrib import admin
from django.urls import path
from schoolapp.views import *
from SMS  import settings
from django.conf.urls.static import static

urlpatterns = [
    path('test/', test, name="test"),
    path('admin/', admin.site.urls),
    #================= log-in /logout Urls =============================
    path('', Login,name='login'),
    path('logout_user', LogoutUser, name='logout_user'),


    #================= Admin Urls ===================================
    path('admin_dashboard/', AdminDashboard ,name='admin_dashboard'),

   
    #Student
    path('admin_side/add_student/', AddStudent ,name='add_student'),
    path('admin_side/edit_student/<int:student_id>', EditStudent ,name='edit_student'),
    path('delete_student/<student_id>', DeleteStudent ,name='delete_student'),
    path('admin_side/list_student/', ListStudent ,name='list_student'),

    #Teacher
    path('admin_side/add_teacher/', AddTeacher ,name='add_teacher'),
    path('admin_side/edit_teacher/<int:teacher_id>', EditTeacher ,name='edit_teacher'),
    path('delete_teacher/<int:teacher_id>', DeleteTeacher ,name='delete_teacher'),
    path('admin_side/list_teacher/', ListTeacher ,name='list_teacher'),

    #Class
    path('admin_side/add_class/', AddClass ,name='add_class'),
    path('admin_side/edit_class/<int:class_id>', EditClass ,name='edit_class'),
    path('admin_side/delete_class/<int:class_id>', DeleteClass ,name='delete_class'),
    path('admin_side/list_class/', ListClass ,name='list_class'),

    #Subject
    path('admin_side/add_subject/', AddSubject ,name='add_subject'),
    path('admin_side/edit_subject/<int:subject_id>', EditSubject ,name='edit_subject'),
    path('admin_side/delete_subject/<int:subject_id>', DeleteSubject ,name='delete_subject'),
    path('admin_side/list_subject/', ListSubject ,name='list_subject'),

    #Timetable
    path('admin_side/add_timetable/', AddTimetable ,name='add_timetable'),
    path('admin_side/edit_timetable/', EditTimetable ,name='edit_timetable'),
    path('admin_side/delete_timetable/', DeleteTimetable ,name='delete_timetable'),
    path('admin_side/list_timetable/', ListTimetable ,name='list_timetable'),

    #Holiday
    path('admin_side/add_holiday/', AddHoliday ,name='add_holiday'),
    path('admin_side/edit_holiday/<int:holiday_id>', EditHoliday ,name='edit_holiday'),
    path('delete_holiday/<int:holiday_id>', DeleteHoliday ,name='delete_holiday'),
    path('admin_side/list_holiday/', ListHoliday ,name='list_holiday'),

 
    #library
    path('add_library/', AddLibrary ,name='add_library'),
    path('edit_library/', EditLibrary ,name='edit_library'),
    path('delete_library/', DeleteLibrary ,name='delete_library'),
    path('list_library/', ListLibrary ,name='list_library'),


    #leave
    path('Admin/Teacher/View_leave', AdminViewTeacher , name='admin_view_teacher_leave'),

    path('Admin/Teacher/Approve_leave/<str:id>', AdminApproveTeacher , name='admin_approve_teacher_leave'),
    path('Admin/Teacher/disapprove_leave/<str:id>', AdminDisapproveTeacher , name='admin_disapprove_teacher_leave'),


    #================= Teacher Urls =================================
    path('teacher_dashboard/', TeacherDashboard ,name='teacher_dashboard'),

    #Attendance
    path('teacher/take_attendance/',TakeAttendance, name='take_attendance'),

    #Exam
    path('teacher/add_exam/', AddExam ,name='add_exam'),
    path('teacher/edit_exam/<int:exam_id>', EditExam ,name='edit_exam'),
    path('teacher/delete_exam/<int:exam_id>', DeleteExam ,name='delete_exam'),
    path('teacher/list_exam/', ListExam ,name='list_exam'),

    #Result
    path('teacher/add_result/', AddResult ,name='add_result'),
    path('teacher/edit_result/<int:result_id>', EditResult ,name='edit_result'),
    path('teacher/delete_result/<int:result_id>', DeleteResult ,name='delete_result'),
    path('teacher/list_result/', ListResult ,name='list_result'),

    #Leave
    path('teacher/apply_leave/', TeacherLeave ,name='teacher_apply_leave'),
    path('teacher/view_leave_history/', TeacherViewLeave ,name='teacher_view_leave_history'),


    #================= Student Urls =================================
    path('student_dashboard/', StudentDashboard ,name='student_dashboard'),


    #================= Other Urls ===================================
    path('user_profile/', UserProfile ,name='user_profile'),
    path('admin_side/send_mail/', SendMail ,name='send_mail'),


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
