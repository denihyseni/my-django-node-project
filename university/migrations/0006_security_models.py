"""
Migration for security models - Token tracking and session management
"""
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('university', '0005_dummy_data'),
    ]

    operations = [
        # TokenBlacklist model
        migrations.CreateModel(
            name='TokenBlacklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField()),
                ('blacklisted_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('reason', models.CharField(choices=[('logout', 'User Logout'), ('rotation', 'Token Rotation'), ('security', 'Security Issue'), ('password_change', 'Password Changed')], default='logout', max_length=50)),
            ],
            options={
                'verbose_name': 'Blacklisted Token',
                'verbose_name_plural': 'Blacklisted Tokens',
            },
        ),
        # Add indexes to TokenBlacklist
        migrations.AddIndex(
            model_name='tokenblacklist',
            index=models.Index(fields=['token'], name='university_t_token_1a2b3c_idx'),
        ),
        migrations.AddIndex(
            model_name='tokenblacklist',
            index=models.Index(fields=['expires_at'], name='university_t_expires_1a2b3d_idx'),
        ),
        
        # UserSession model
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_jti', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_activity', models.DateTimeField(auto_now=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.TextField(blank=True)),
                ('device_name', models.CharField(blank=True, max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Session',
                'verbose_name_plural': 'User Sessions',
                'ordering': ['-last_activity'],
            },
        ),
        # Add indexes to UserSession
        migrations.AddIndex(
            model_name='usersession',
            index=models.Index(fields=['user', 'is_active'], name='university_u_user_id_1a2b3e_idx'),
        ),
        migrations.AddIndex(
            model_name='usersession',
            index=models.Index(fields=['token_jti'], name='university_u_token_1a2b3f_idx'),
        ),
        
        # LoginAttempt model
        migrations.CreateModel(
            name='LoginAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.TextField(blank=True)),
                ('attempted_at', models.DateTimeField(auto_now_add=True)),
                ('success', models.BooleanField(default=False)),
                ('failure_reason', models.CharField(blank=True, choices=[('invalid_credentials', 'Invalid Credentials'), ('user_inactive', 'User Inactive'), ('user_not_found', 'User Not Found'), ('rate_limit', 'Rate Limited'), ('other', 'Other')], max_length=100)),
            ],
            options={
                'verbose_name': 'Login Attempt',
                'verbose_name_plural': 'Login Attempts',
                'ordering': ['-attempted_at'],
            },
        ),
        # Add indexes to LoginAttempt
        migrations.AddIndex(
            model_name='loginattempt',
            index=models.Index(fields=['ip_address', 'attempted_at'], name='university_l_ip_addr_1a2b40_idx'),
        ),
        migrations.AddIndex(
            model_name='loginattempt',
            index=models.Index(fields=['username', 'attempted_at'], name='university_l_usernam_1a2b41_idx'),
        ),
        
        # SecurityEvent model
        migrations.CreateModel(
            name='SecurityEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(choices=[('token_refresh', 'Token Refresh'), ('token_revocation', 'Token Revocation'), ('logout', 'Logout'), ('login', 'Login'), ('failed_login', 'Failed Login'), ('permission_denied', 'Permission Denied'), ('suspicious_activity', 'Suspicious Activity'), ('password_change', 'Password Change'), ('mfa_enabled', 'MFA Enabled'), ('session_terminated', 'Session Terminated')], max_length=50)),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('severity', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')], default='low', max_length=20)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Security Event',
                'verbose_name_plural': 'Security Events',
                'ordering': ['-timestamp'],
            },
        ),
        # Add indexes to SecurityEvent
        migrations.AddIndex(
            model_name='securityevent',
            index=models.Index(fields=['user', 'timestamp'], name='university_s_user_id_1a2b42_idx'),
        ),
        migrations.AddIndex(
            model_name='securityevent',
            index=models.Index(fields=['severity', 'timestamp'], name='university_s_severit_1a2b43_idx'),
        ),
    ]
