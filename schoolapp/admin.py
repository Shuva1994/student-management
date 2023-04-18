from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from schoolapp.models import *

class UserModel(UserAdmin):
    list_display = ['username','user_type']

admin.site.register(CustomUser,UserModel)
admin.site.register(Class)
admin.site.register(Session_Year)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Section)