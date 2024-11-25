from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as auth_views
from django.views.generic import RedirectView  # Import RedirectView
from attendance_backend import views as attendance_views

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'courses', attendance_views.CourseViewSet)
router.register(r'semesters', attendance_views.SemesterViewSet)
router.register(r'lecturers', attendance_views.LecturerViewSet)
router.register(r'students', attendance_views.StudentViewSet)
router.register(r'classes', attendance_views.ClassViewSet)
router.register(r'college_days', attendance_views.CollegeDayViewSet)
router.register(r'enrollments', attendance_views.EnrollmentViewSet)

# Define URL patterns
urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=True)),  # Redirect root URL to admin
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/api-token-auth/', auth_views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls')),
]
