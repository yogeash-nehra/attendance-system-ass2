from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    credits = models.IntegerField()  # Number of credits for the course

    def __str__(self):
        return self.name

class Semester(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class Lecturer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Class(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} - {self.course.name} ({self.semester.name})"

class CollegeDay(models.Model):
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    classes = models.ManyToManyField(Class)

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"

# New model for Attendance
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student} - {self.class_instance} on {self.date} ({self.status})"
