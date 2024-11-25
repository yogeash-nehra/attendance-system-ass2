from django.contrib import admin
from .models import Course, Semester, Lecturer, Student, Class, CollegeDay, Enrollment

admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(Lecturer)
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(CollegeDay)
admin.site.register(Enrollment)
