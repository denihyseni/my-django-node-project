from django.contrib import admin
from . import models
from .security_models import TokenBlacklist, UserSession, LoginAttempt, SecurityEvent


@admin.register(models.Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('user', 'faculty', 'office')


@admin.register(models.Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('user', 'faculty', 'title')


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'faculty', 'enrollment_number')


@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty', 'professor', 'credits', 'max_students')


@admin.register(models.Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'grade', 'score', 'enrolled_date')
    readonly_fields = ('enrolled_date',)
    list_filter = ('subject__faculty', 'grade')
    search_fields = ('student__user__username', 'subject__name')


# ===== SECURITY MODELS ADMIN =====

@admin.register(TokenBlacklist)
class TokenBlacklistAdmin(admin.ModelAdmin):
    list_display = ('blacklisted_at', 'expires_at', 'reason')
    readonly_fields = ('token', 'blacklisted_at')
    list_filter = ('reason', 'blacklisted_at')
    ordering = ('-blacklisted_at',)
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'created_at', 'last_activity', 'is_active')
    readonly_fields = ('user', 'created_at', 'last_activity', 'ip_address', 'user_agent', 'token_jti')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username', 'ip_address')
    ordering = ('-last_activity',)
    
    def has_add_permission(self, request):
        return False


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('username', 'ip_address', 'attempted_at', 'success', 'failure_reason')
    readonly_fields = ('username', 'ip_address', 'user_agent', 'attempted_at', 'success', 'failure_reason')
    list_filter = ('success', 'attempted_at', 'failure_reason')
    search_fields = ('username', 'ip_address')
    ordering = ('-attempted_at',)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'user', 'ip_address', 'timestamp', 'severity')
    readonly_fields = ('user', 'event_type', 'ip_address', 'user_agent', 'description', 'timestamp', 'severity')
    list_filter = ('event_type', 'severity', 'timestamp')
    search_fields = ('user__username', 'ip_address')
    ordering = ('-timestamp',)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

