"""
Token Security Models - For tracking token blacklists and user sessions
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class TokenBlacklist(models.Model):
    """Track revoked/blacklisted tokens"""
    token = models.TextField()
    blacklisted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    reason = models.CharField(
        max_length=50,
        choices=[
            ('logout', 'User Logout'),
            ('rotation', 'Token Rotation'),
            ('security', 'Security Issue'),
            ('password_change', 'Password Changed'),
        ],
        default='logout'
    )
    
    class Meta:
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['expires_at']),
        ]
        verbose_name = "Blacklisted Token"
        verbose_name_plural = "Blacklisted Tokens"
    
    def __str__(self):
        return f"Token blacklisted: {self.blacklisted_at}"
    
    @classmethod
    def clean_expired(cls):
        """Remove expired tokens from blacklist"""
        cls.objects.filter(expires_at__lt=timezone.now()).delete()


class UserSession(models.Model):
    """Track active user sessions for security monitoring"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    token_jti = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    device_name = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-last_activity']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['token_jti']),
        ]
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"
    
    def __str__(self):
        return f"{self.user.username} - {self.ip_address} - {self.created_at}"
    
    def is_expired(self):
        """Check if session has expired (7 days)"""
        return timezone.now() - self.created_at > timedelta(days=7)
    
    @classmethod
    def clean_expired(cls):
        """Remove expired sessions"""
        cutoff = timezone.now() - timedelta(days=7)
        cls.objects.filter(created_at__lt=cutoff).delete()


class LoginAttempt(models.Model):
    """Track login attempts for security monitoring"""
    username = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    attempted_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    failure_reason = models.CharField(
        max_length=100,
        blank=True,
        choices=[
            ('invalid_credentials', 'Invalid Credentials'),
            ('user_inactive', 'User Inactive'),
            ('user_not_found', 'User Not Found'),
            ('rate_limit', 'Rate Limited'),
            ('other', 'Other'),
        ]
    )
    
    class Meta:
        ordering = ['-attempted_at']
        indexes = [
            models.Index(fields=['ip_address', 'attempted_at']),
            models.Index(fields=['username', 'attempted_at']),
        ]
        verbose_name = "Login Attempt"
        verbose_name_plural = "Login Attempts"
    
    def __str__(self):
        status = "Success" if self.success else "Failed"
        return f"{self.username} - {status} - {self.attempted_at}"
    
    @classmethod
    def is_rate_limited(cls, ip_address, max_attempts=5, window_minutes=15):
        """Check if IP is rate limited"""
        cutoff = timezone.now() - timedelta(minutes=window_minutes)
        recent_attempts = cls.objects.filter(
            ip_address=ip_address,
            success=False,
            attempted_at__gte=cutoff
        ).count()
        if settings.DEBUG:
            return False
        return recent_attempts >= max_attempts
    
    @classmethod
    def clean_old(cls):
        """Remove login attempts older than 30 days"""
        cutoff = timezone.now() - timedelta(days=30)
        cls.objects.filter(attempted_at__lt=cutoff).delete()


class SecurityEvent(models.Model):
    """Log security-related events"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    event_type = models.CharField(
        max_length=50,
        choices=[
            ('token_refresh', 'Token Refresh'),
            ('token_revocation', 'Token Revocation'),
            ('logout', 'Logout'),
            ('login', 'Login'),
            ('failed_login', 'Failed Login'),
            ('permission_denied', 'Permission Denied'),
            ('suspicious_activity', 'Suspicious Activity'),
            ('password_change', 'Password Change'),
            ('mfa_enabled', 'MFA Enabled'),
            ('session_terminated', 'Session Terminated'),
        ]
    )
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        default='low'
    )
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['severity', 'timestamp']),
        ]
        verbose_name = "Security Event"
        verbose_name_plural = "Security Events"
    
    def __str__(self):
        return f"{self.event_type} - {self.user} - {self.timestamp}"
    
    @classmethod
    def log_event(cls, event_type, request, user=None, description='', severity='low'):
        """Log a security event"""
        cls.objects.create(
            user=user,
            event_type=event_type,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            description=description,
            severity=severity
        )
    
    @classmethod
    def clean_old(cls):
        """Remove events older than 90 days"""
        cutoff = timezone.now() - timedelta(days=90)
        cls.objects.filter(timestamp__lt=cutoff).delete()


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
