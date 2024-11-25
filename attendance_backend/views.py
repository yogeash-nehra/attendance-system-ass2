from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Course, Semester, Lecturer, Student, Class, CollegeDay, Enrollment, Attendance
from .serializers import (
    CourseSerializer, SemesterSerializer, LecturerSerializer,
    StudentSerializer, ClassSerializer, CollegeDaySerializer, EnrollmentSerializer, AttendanceSerializer
)
from .permissions import IsAdminUser, IsLecturerUser, IsStudentUser



class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Only Admin users


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Only Admin users


class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def assign_class(self, request, pk=None):
        """
        Custom action to assign a class to a lecturer.
        """
        lecturer = self.get_object()
        class_id = request.data.get("class_id")
        try:
            class_instance = Class.objects.get(id=class_id)
            class_instance.lecturer = lecturer
            class_instance.save()
            return Response({"status": "Class assigned to lecturer successfully"})
        except Class.DoesNotExist:
            return Response({"error": "Class not found"}, status=status.HTTP_400_BAD_REQUEST)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Only Admin users for managing students

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def enroll(self, request, pk=None):
        """
        Custom action to enroll a student in a course.
        """
        student = self.get_object()
        course_id = request.data.get("course_id")
        try:
            course = Course.objects.get(id=course_id)
            Enrollment.objects.create(student=student, course=course)
            return Response({"status": "Student enrolled in course successfully"})
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_400_BAD_REQUEST)


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Only Admin users


class CollegeDayViewSet(viewsets.ModelViewSet):
    queryset = CollegeDay.objects.all()
    serializer_class = CollegeDaySerializer
    permission_classes = [IsAuthenticated, IsLecturerUser]  # Only Lecturers can access CollegeDay actions

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsLecturerUser])
    def assign_class(self, request, pk=None):
        """
        Custom action to assign a class to a CollegeDay.
        """
        college_day = self.get_object()
        class_id = request.data.get("class_id")
        try:
            class_instance = Class.objects.get(id=class_id)
            college_day.classes.add(class_instance)
            college_day.save()
            return Response({"status": "Class assigned to College Day successfully"})
        except Class.DoesNotExist:
            return Response({"error": "Class not found"}, status=status.HTTP_400_BAD_REQUEST)


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsStudentUser]  # Only Students can view their enrollments

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsStudentUser])
    def my_enrollments(self, request):
        """
        Custom action for students to view their enrollments.
        """
        student = request.user.student_profile  # Assuming user has a related student profile
        enrollments = Enrollment.objects.filter(student=student)
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsLecturerUser]

    @action(detail=False, methods=['post'], permission_classes=[IsLecturerUser])
    def mark_attendance(self, request):
        """
        Custom action for lecturers to mark attendance for students.
        """
        student_id = request.data.get("student_id")
        class_id = request.data.get("class_id")
        date = request.data.get("date")
        status = request.data.get("status")
        try:
            student = Student.objects.get(id=student_id)
            class_instance = Class.objects.get(id=class_id)
            Attendance.objects.create(student=student, class_instance=class_instance, date=date, status=status)
            return Response({"status": "Attendance marked successfully"})
        except (Student.DoesNotExist, Class.DoesNotExist):
            return Response({"error": "Student or Class not found"}, status=status.HTTP_400_BAD_REQUEST)
