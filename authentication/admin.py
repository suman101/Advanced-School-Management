from itertools import count
from django.contrib import admin
from .models import HomePageSchoolAdmin, ImageGallary, User, SchoolProfile, TeacherProfile, StudentProfile
# Register your models here.
# admin.site.register(User)
admin.site.register(ImageGallary)
admin.site.register(TeacherProfile)
admin.site.register(HomePageSchoolAdmin)
# admin.site.register(StudentProfile)
#admin.site.register(LibrarianProfile)

@admin.register(SchoolProfile)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['id','school_name','school_type','phone_number','address','school_website']
    list_display_links = ['school_name']
    class Meta:
        model = SchoolProfile
        verbose_name = "School List"

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','school','phone_number','email','user_type']
    list_display_links = ['username']
    class Meta:
        model = User


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','father_name','grade']
    list_display_links = ['user']
    class Meta:
        model = StudentProfile