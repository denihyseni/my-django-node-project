from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from . import models, serializers


# Custom Permission Classes
class IsAdministrator(BasePermission):
    """Allow access only to Administrators."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'administrator')
        )


class IsAdminOrReadOnly(BasePermission):
    """Allow write access to Admins, read access to authenticated users."""
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user and request.user.is_authenticated
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'administrator')
        )
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return hasattr(request.user, 'administrator')


class IsAdminOrProfessor(BasePermission):
    """Allow access to Admins and Professors."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (
                hasattr(request.user, 'administrator')
                or hasattr(request.user, 'professor')
            )
        )


class IsOwnProfileOrAdmin(BasePermission):
    """Allow users to view/edit their own profile, or Admins full access."""
    def has_object_permission(self, request, view, obj):
        # Admin can do anything
        if hasattr(request.user, 'administrator'):
            return True
        # User can only access their own profile
        return obj.user == request.user



class FacultyViewSet(viewsets.ModelViewSet):
    queryset = models.Faculty.objects.all()
    serializer_class = serializers.FacultySerializer
    permission_classes = [IsAdminOrReadOnly]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = models.Subject.objects.all()
    serializer_class = serializers.SubjectSerializer
    permission_classes = [IsAdminOrReadOnly]


class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = models.Professor.objects.all()
    serializer_class = serializers.ProfessorSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return serializers.ProfessorCreateUpdateSerializer
        return serializers.ProfessorSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return serializers.StudentCreateUpdateSerializer
        return serializers.StudentSerializer


class AdministratorViewSet(viewsets.ModelViewSet):
    queryset = models.Administrator.objects.all()
    serializer_class = serializers.AdministratorSerializer
    permission_classes = [IsAdministrator]

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return serializers.AdministratorCreateUpdateSerializer
        return serializers.AdministratorSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    """Handle student enrollments and grade management."""
    queryset = models.Enrollment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.EnrollmentDetailSerializer
        return serializers.EnrollmentSerializer

    def get_queryset(self):
        """Filter enrollments based on user role."""
        user = self.request.user
        if hasattr(user, 'administrator'):
            # Admin sees all enrollments
            return models.Enrollment.objects.all()
        elif hasattr(user, 'professor'):
            # Professor sees enrollments in their courses
            prof = user.professor
            return models.Enrollment.objects.filter(subject__professor=prof)
        elif hasattr(user, 'student'):
            # Student sees only their enrollments
            student = user.student
            return models.Enrollment.objects.filter(student=student)
        return models.Enrollment.objects.none()

    def get_permissions(self):
        """Allow students to create their own enrollments, professors to grade."""
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update']:
            # Admins and professors can update (for grading)
            return [IsAdminOrProfessor()]
        elif self.action == 'destroy':
            return [IsAdministrator()]
        return super().get_permissions()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    user = request.user
    # Determine role by presence of related profile
    role = 'user'
    if hasattr(user, 'administrator'):
        role = 'administrator'
    elif hasattr(user, 'professor'):
        role = 'professor'
    elif hasattr(user, 'student'):
        role = 'student'

    data = {
        'username': user.username,
        'role': role,
    }
    
    # Admin: return summary statistics
    if role == 'administrator':
        data['total_students'] = models.Student.objects.count()
        data['total_professors'] = models.Professor.objects.count()
        data['total_subjects'] = models.Subject.objects.count()
        data['total_enrollments'] = models.Enrollment.objects.count()
    
    # Professor: return their courses
    if role == 'professor':
        prof = user.professor
        courses = prof.subjects.all()
        data['courses'] = [
            {
                'id': c.id,
                'name': c.name,
                'students_count': c.enrollments.count(),
                'credits': c.credits,
            }
            for c in courses
        ]
    
    # Student: return their enrollments
    if role == 'student':
        student = user.student
        enrollments = student.enrollments.all()
        data['enrollments'] = [
            {
                'id': e.id,
                'subject': e.subject.name,
                'professor': e.subject.professor.user.get_full_name() or e.subject.professor.user.username,
                'grade': e.grade or 'Not Graded',
                'score': e.score,
            }
            for e in enrollments
        ]

    return Response(data)

