from rest_framework import serializers
from .models import Course, Semester, Lecturer, Student, Class, CollegeDay, Enrollment, Attendance


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'credits']  # Include credits based on model


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'name', 'start_date', 'end_date']


class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = ['id', 'first_name', 'last_name', 'email']


class StudentSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)  # Nested courses for each student

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email', 'enrollment_date', 'courses']  # Added enrollment_date


class ClassSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())  # Accept course ID
    semester = serializers.PrimaryKeyRelatedField(queryset=Semester.objects.all())  # Accept semester ID
    lecturer = serializers.PrimaryKeyRelatedField(queryset=Lecturer.objects.all())  # Accept lecturer ID

    class Meta:
        model = Class
        fields = ['id', 'name', 'course', 'semester', 'lecturer']


class CollegeDaySerializer(serializers.ModelSerializer):
    classes = ClassSerializer(many=True, read_only=True)  # Many-to-many nested serializer for classes

    class Meta:
        model = CollegeDay
        fields = ['id', 'date', 'description', 'classes']


class EnrollmentSerializer(serializers.ModelSerializer):
    student = StudentSerializer()  # Nested serializer for student
    course = CourseSerializer()  # Nested serializer for course

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrollment_date']

class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    class_instance = ClassSerializer()

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'class_instance', 'date', 'status']