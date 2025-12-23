# Generated migration - adds dummy data for testing all features

from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_dummy_data(apps, schema_editor):
    """Create dummy courses and enrollments for testing."""
    Subject = apps.get_model('university', 'Subject')
    Student = apps.get_model('university', 'Student')
    Professor = apps.get_model('university', 'Professor')
    Faculty = apps.get_model('university', 'Faculty')
    Enrollment = apps.get_model('university', 'Enrollment')
    User = apps.get_model('auth', 'User')

    # Get faculties
    try:
        cs_faculty = Faculty.objects.get(name='CS')
        en_faculty = Faculty.objects.get(name='EN')
    except Faculty.DoesNotExist:
        return

    # Create additional professors
    professors_data = [
        {'username': 'prof_smith', 'email': 'smith@uni.edu', 'faculty': cs_faculty, 'title': 'Dr.'},
        {'username': 'prof_johnson', 'email': 'johnson@uni.edu', 'faculty': en_faculty, 'title': 'Prof.'},
    ]
    
    for prof_data in professors_data:
        user, _ = User.objects.get_or_create(
            username=prof_data['username'],
            defaults={
                'email': prof_data['email'],
                'password': make_password('prof123'),
            }
        )
        if not Professor.objects.filter(user=user).exists():
            Professor.objects.create(
                user=user,
                faculty=prof_data['faculty'],
                title=prof_data['title']
            )

    # Create additional students
    students_data = [
        {'username': 'student2', 'email': 'student2@uni.edu', 'faculty': cs_faculty, 'enroll_num': 'CS102'},
        {'username': 'student3', 'email': 'student3@uni.edu', 'faculty': cs_faculty, 'enroll_num': 'CS103'},
        {'username': 'student4', 'email': 'student4@uni.edu', 'faculty': en_faculty, 'enroll_num': 'EN101'},
    ]

    for student_data in students_data:
        user, _ = User.objects.get_or_create(
            username=student_data['username'],
            defaults={
                'email': student_data['email'],
                'password': make_password('student123'),
            }
        )
        if not Student.objects.filter(user=user).exists():
            Student.objects.create(
                user=user,
                faculty=student_data['faculty'],
                enrollment_number=student_data['enroll_num']
            )

    # Get the professors
    prof_1 = Professor.objects.get(user__username='professor1')  # Original
    prof_smith = Professor.objects.get(user__username='prof_smith')
    prof_johnson = Professor.objects.get(user__username='prof_johnson')

    # Create subjects (courses)
    courses = [
        {
            'name': 'Data Structures',
            'description': 'Advanced data structures and algorithms',
            'faculty': cs_faculty,
            'professor': prof_1,
            'credits': 4,
            'max_students': 30,
        },
        {
            'name': 'Database Systems',
            'description': 'Relational databases and SQL',
            'faculty': cs_faculty,
            'professor': prof_smith,
            'credits': 3,
            'max_students': 25,
        },
        {
            'name': 'Web Development',
            'description': 'Full-stack web development with Django and React',
            'faculty': cs_faculty,
            'professor': prof_smith,
            'credits': 3,
            'max_students': 30,
        },
        {
            'name': 'Modern Poetry',
            'description': 'Analysis of 20th and 21st century poetry',
            'faculty': en_faculty,
            'professor': prof_johnson,
            'credits': 3,
            'max_students': 20,
        },
        {
            'name': 'Creative Writing',
            'description': 'Fiction, non-fiction, and poetry composition',
            'faculty': en_faculty,
            'professor': prof_johnson,
            'credits': 3,
            'max_students': 15,
        },
    ]

    for course in courses:
        subject, _ = Subject.objects.get_or_create(
            name=course['name'],
            defaults={
                'description': course['description'],
                'faculty': course['faculty'],
                'professor': course['professor'],
                'credits': course['credits'],
                'max_students': course['max_students'],
            }
        )

    # Get all subjects
    ds_course = Subject.objects.get(name='Data Structures')
    db_course = Subject.objects.get(name='Database Systems')
    web_course = Subject.objects.get(name='Web Development')
    poetry_course = Subject.objects.get(name='Modern Poetry')
    writing_course = Subject.objects.get(name='Creative Writing')

    # Get all students
    student_1 = Student.objects.get(user__username='student1')
    student_2 = Student.objects.get(user__username='student2')
    student_3 = Student.objects.get(user__username='student3')
    student_4 = Student.objects.get(user__username='student4')

    # Create enrollments with grades
    enrollments = [
        # Student 1 (CS) - enrolled in CS courses
        {'student': student_1, 'subject': ds_course, 'grade': 'A', 'score': 92},
        {'student': student_1, 'subject': db_course, 'grade': 'B', 'score': 85},
        {'student': student_1, 'subject': web_course, 'grade': 'A', 'score': 95},
        # Student 2 (CS) - enrolled in some CS courses
        {'student': student_2, 'subject': ds_course, 'grade': 'B', 'score': 88},
        {'student': student_2, 'subject': db_course, 'grade': 'B', 'score': 82},
        # Student 3 (CS) - enrolled in different courses
        {'student': student_3, 'subject': ds_course, 'grade': 'C', 'score': 75},
        {'student': student_3, 'subject': web_course, 'grade': 'B', 'score': 84},
        # Student 4 (EN) - enrolled in English courses
        {'student': student_4, 'subject': poetry_course, 'grade': 'A', 'score': 91},
        {'student': student_4, 'subject': writing_course, 'grade': 'A', 'score': 94},
    ]

    for enroll in enrollments:
        Enrollment.objects.get_or_create(
            student=enroll['student'],
            subject=enroll['subject'],
            defaults={
                'grade': enroll['grade'],
                'score': enroll['score'],
            }
        )


def reverse_dummy_data(apps, schema_editor):
    """Remove dummy data."""
    Subject = apps.get_model('university', 'Subject')
    Enrollment = apps.get_model('university', 'Enrollment')
    User = apps.get_model('auth', 'User')
    
    # Delete enrollments first (FK constraint)
    Enrollment.objects.all().delete()
    
    # Delete courses
    Subject.objects.filter(name__in=[
        'Data Structures', 'Database Systems', 'Web Development',
        'Modern Poetry', 'Creative Writing'
    ]).delete()
    
    # Delete additional professors and students
    User.objects.filter(username__in=[
        'prof_smith', 'prof_johnson',
        'student2', 'student3', 'student4'
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0004_remove_subject_students_subject_credits_and_more'),
    ]

    operations = [
        migrations.RunPython(create_dummy_data, reverse_dummy_data),
    ]
