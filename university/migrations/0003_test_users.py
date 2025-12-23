# Generated migration - adds test users with different roles

from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_test_users(apps, schema_editor):
    """Create test users: admin, professor, and student."""
    Administrator = apps.get_model('university', 'Administrator')
    Professor = apps.get_model('university', 'Professor')
    Student = apps.get_model('university', 'Student')
    Faculty = apps.get_model('university', 'Faculty')
    User = apps.get_model('auth', 'User')

    # Get Computer Science faculty
    try:
        cs_faculty = Faculty.objects.get(name='CS')
    except Faculty.DoesNotExist:
        return  # Faculty not created yet

    # Create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin_user',
        defaults={
            'email': 'admin@university.edu',
            'is_staff': True,
            'is_superuser': False,
            'password': make_password('admin123'),
        }
    )
    
    # Create admin profile if not exists
    if not Administrator.objects.filter(user=admin_user).exists():
        Administrator.objects.create(user=admin_user, faculty=cs_faculty)

    # Create professor user
    prof_user, created = User.objects.get_or_create(
        username='professor1',
        defaults={
            'email': 'professor1@university.edu',
            'password': make_password('prof123'),
        }
    )
    
    # Create professor profile if not exists
    if not Professor.objects.filter(user=prof_user).exists():
        Professor.objects.create(user=prof_user, faculty=cs_faculty)

    # Create student user
    student_user, created = User.objects.get_or_create(
        username='student1',
        defaults={
            'email': 'student1@university.edu',
            'password': make_password('student123'),
        }
    )
    
    # Create student profile if not exists
    if not Student.objects.filter(user=student_user).exists():
        Student.objects.create(user=student_user, faculty=cs_faculty)


def reverse_test_users(apps, schema_editor):
    """Remove test users."""
    User = apps.get_model('auth', 'User')
    User.objects.filter(username__in=['admin_user', 'professor1', 'student1']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0002_initial_data'),
    ]

    operations = [
        migrations.RunPython(create_test_users, reverse_test_users),
    ]
