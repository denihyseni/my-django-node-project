from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'faculties', views.FacultyViewSet)
router.register(r'subjects', views.SubjectViewSet)
router.register(r'professors', views.ProfessorViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'administrators', views.AdministratorViewSet)
router.register(r'enrollments', views.EnrollmentViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', views.dashboard, name='dashboard'),
]