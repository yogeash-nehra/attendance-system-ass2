from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from attendance_backend import views

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'semesters', views.SemesterViewSet)
router.register(r'lecturers', views.LecturerViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'classes', views.ClassViewSet)
router.register(r'college_days', views.CollegeDayViewSet)
router.register(r'attendance', views.AttendanceViewSet)
router.register(r'enrollments', views.EnrollmentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Include all the registered viewsets
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', include('rest_framework.authtoken.urls')),  # For token authentication
]
