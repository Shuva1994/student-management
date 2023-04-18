from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER =(
        (1,'ADMIN'),
        (2,'TEACHER'),
        (3,'STUDENT'),
    )
    user_type = models.CharField(choices=USER,default=1,max_length=50)
    profile_pic = models.ImageField(upload_to='media/profile_pic')



class Class(models.Model):     
    name = models.CharField(max_length=300, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    Updated_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Session_Year(models.Model): 
    session_start= models.CharField(max_length=100)
 
    def __str__(self):
        return self.session_start
    
class Section(models.Model): 
    section_name= models.CharField(max_length=100)
 
    def __str__(self):
        return self.section_name  


class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender= models.CharField(max_length=255,null=True)
    dob= models.DateField(null=True)
    guardian_name = models.CharField(max_length=255,null=True)
    guardian_contact = models.CharField(max_length=255,null=False)
    contact= models.CharField(max_length=255,null=True)
    address= models.TextField(null=True)
    roll_no = models.CharField(max_length=255,null=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.first_name
    

class Teacher(models.Model):
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address = models.TextField(max_length=250,null=True)
    gender = models.CharField(max_length=100,null=True)
    dob= models.DateField(null=True)
    doj =models.DateField(null=True)
    phone= models.CharField(max_length=255,null=True)
    qualification= models.CharField(max_length=100,null=True)
    experience= models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.username

class Holiday(models.Model):
    holiday_name = models.CharField(max_length=100)
    holiday_type = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.holiday_name
    

class Subject(models.Model):
    name = models.CharField(max_length=100)
    classs = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Attendance(models.Model):
    session = models.ForeignKey(Session_Year, on_delete=models.DO_NOTHING)
    clas = models.ForeignKey(Class, on_delete=models.DO_NOTHING)
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    is_present =models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject.name

class Attendance_Report(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance= models.ForeignKey(Attendance, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.admin.first_name


class Teacher_Leave(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    No_of_days = models.CharField(max_length=100,null=True)
    leave_type = models.CharField(max_length=100,null=True)
    details = models.CharField(max_length=100,null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.teacher.admin.first_name
    

class Exam(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.name


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    Total_marks = models.IntegerField()
    marks = models.IntegerField()

    def __str__(self):
        return self.student.admin.first_name