from django.db import migrations


def create_initial_data(apps, schema_editor):
    Faculty = apps.get_model('university', 'Faculty')
    User = apps.get_model('auth', 'User')

    # Create faculties if they don't exist
    Faculty.objects.get_or_create(name='CS')
    Faculty.objects.get_or_create(name='EN')

    # Create default admin user
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')


def reverse_func(apps, schema_editor):
    Faculty = apps.get_model('university', 'Faculty')
    User = apps.get_model('auth', 'User')
    Faculty.objects.filter(name__in=['CS', 'EN']).delete()
    User.objects.filter(username='admin').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data, reverse_func),
    ]
