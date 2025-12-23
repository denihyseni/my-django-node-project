from django.db import models
from django.contrib.auth.models import User


class Faculty(models.Model):
    COMPUTER_SCIENCE = 'CS'
    ENGLISH = 'EN'
    DEPARTMENT_CHOICES = [
        (COMPUTER_SCIENCE, 'Computer Science'),
        (ENGLISH, 'English'),
    ]

    name = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, unique=True)

    def __str__(self):
        return dict(self.DEPARTMENT_CHOICES).get(self.name, self.name)


class BaseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True


class Administrator(BaseProfile):
    office = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'Administrator: {self.user.username}'


class Professor(BaseProfile):
    title = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'Professor: {self.user.username}'


class Student(BaseProfile):
    enrollment_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'Student: {self.user.username}'


class Subject(models.Model):
    name = models.CharField(max_length=200)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='subjects')
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, related_name='subjects')
    description = models.TextField(blank=True)
    credits = models.IntegerField(default=3)
    max_students = models.IntegerField(default=30)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    """Tracks student enrollment in courses."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_date = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(
        max_length=2,
        choices=[
            ('A', 'A (90-100)'),
            ('B', 'B (80-89)'),
            ('C', 'C (70-79)'),
            ('D', 'D (60-69)'),
            ('F', 'F (Below 60)'),
            ('', 'Not Graded'),
        ],
        default='',
        blank=True
    )
    score = models.FloatField(null=True, blank=True)  # Numerical score 0-100

    class Meta:
        unique_together = ('student', 'subject')

    def __str__(self):
        return f'{self.student.user.username} enrolled in {self.subject.name}'
