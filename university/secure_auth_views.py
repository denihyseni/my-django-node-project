"""
Secure Authentication Views with HttpOnly Cookie Token Storage
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import authenticate
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging

from .security_models import (
    TokenBlacklist,
    UserSession,
    LoginAttempt,
    SecurityEvent,
    get_client_ip,
)

logger = logging.getLogger(__name__)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# ============================================================
# LOGIN (NO TOKEN REQUIRED)
# ============================================================
@method_decorator(csrf_exempt, name="dispatch")
class SecureTokenObtainView(APIView):
    """
    Secure login endpoint
    """
    permission_classes = [AllowAny]
    authentication_classes = []  # 🔑 CRITICAL

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        ip_address = get_client_ip(request)

        # Rate limiting
        if LoginAttempt.is_rate_limited(ip_address):
            SecurityEvent.log_event(
                "failed_login",
                request,
                description=f"Rate limit exceeded for {username}",
                severity="high",
            )
            return Response(
                {"error": "Too many login attempts. Try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        user = authenticate(username=username, password=password)

        if not user:
            LoginAttempt.objects.create(
                username=username,
                ip_address=ip_address,
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
                success=False,
                failure_reason="invalid_credentials",
            )

            SecurityEvent.log_event(
                "failed_login",
                request,
                description=f"Failed login for {username} from {ip_address}",
                severity="medium",
            )

            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # SUCCESSFUL LOGIN
        tokens = get_tokens_for_user(user)
        access = AccessToken(tokens["access"])

        UserSession.objects.create(
            user=user,
            token_jti=access["jti"],
            ip_address=ip_address,
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
        )

        LoginAttempt.objects.create(
            username=username,
            ip_address=ip_address,
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            success=True,
        )

        SecurityEvent.log_event(
            "login",
            request,
            user=user,
            description=f"User logged in from {ip_address}",
        )

        response = Response(
            {
                "detail": "Login successful",
                "user": user.username,
                "access": tokens["access"],
                "refresh": tokens["refresh"],
            },
            status=status.HTTP_200_OK,
        )

        # HttpOnly cookies
        response.set_cookie(
            "access_token",
            tokens["access"],
            max_age=15 * 60,
            httponly=True,
            secure=not request.scheme == "http",
            samesite="Strict",
            path="/",
        )

        response.set_cookie(
            "refresh_token",
            tokens["refresh"],
            max_age=7 * 24 * 60 * 60,
            httponly=True,
            secure=not request.scheme == "http",
            samesite="Strict",
            path="/",
        )

        return response


# ============================================================
# REFRESH TOKEN (NO AUTH REQUIRED)
# ============================================================
@method_decorator(csrf_exempt, name="dispatch")
class SecureTokenRefreshView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        ip_address = get_client_ip(request)

        if not refresh_token:
            return Response(
                {"error": "No refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if TokenBlacklist.objects.filter(token=refresh_token).exists():
            return Response(
                {"error": "Token revoked"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(refresh_token)

            TokenBlacklist.objects.create(
                token=refresh_token,
                expires_at=timezone.now() + timezone.timedelta(days=7),
                reason="rotation",
            )

            new_refresh = str(refresh)
            new_access = str(refresh.access_token)
            access = AccessToken(new_access)

            UserSession.objects.filter(token_jti=refresh["jti"]).delete()
            UserSession.objects.create(
                user=refresh.user,
                token_jti=access["jti"],
                ip_address=ip_address,
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
            )

            SecurityEvent.log_event(
                "token_refresh",
                request,
                user=refresh.user,
                description=f"Token refreshed from {ip_address}",
            )

            response = Response(
                {"access": new_access, "refresh": new_refresh},
                status=status.HTTP_200_OK,
            )

            response.set_cookie(
                "access_token",
                new_access,
                max_age=15 * 60,
                httponly=True,
                secure=not request.scheme == "http",
                samesite="Strict",
                path="/",
            )

            response.set_cookie(
                "refresh_token",
                new_refresh,
                max_age=7 * 24 * 60 * 60,
                httponly=True,
                secure=not request.scheme == "http",
                samesite="Strict",
                path="/",
            )

            return response

        except (InvalidToken, TokenError):
            return Response(
                {"error": "Invalid refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


# ============================================================
# LOGOUT (AUTH REQUIRED)
# ============================================================
class SecureLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get tokens from cookies
        refresh_token = request.COOKIES.get("refresh_token")
        access_token = request.COOKIES.get("access_token")

        # Blacklist both tokens
        if refresh_token:
            TokenBlacklist.objects.create(
                token=refresh_token,
                expires_at=timezone.now() + timezone.timedelta(days=7),
                reason="logout",
            )

        if access_token:
            TokenBlacklist.objects.create(
                token=access_token,
                expires_at=timezone.now() + timezone.timedelta(minutes=15),
                reason="logout",
            )

        # Delete all sessions for this user
        UserSession.objects.filter(user=request.user).delete()

        # Log the logout event
        SecurityEvent.log_event(
            "logout",
            request,
            user=request.user,
            description="User logged out - all tokens invalidated",
        )

        # Create response and clear cookies
        response = Response({"detail": "Logged out successfully. Please log in again to continue."})
        response.delete_cookie("access_token", path="/", samesite="Strict")
        response.delete_cookie("refresh_token", path="/", samesite="Strict")
        
        # Also clear Django session if any
        request.session.flush() if hasattr(request, 'session') else None
        
        return response


# ============================================================
# SESSION MANAGEMENT
# ============================================================
class SessionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = UserSession.objects.filter(user=request.user).values(
            "id", "ip_address", "user_agent", "created_at", "last_activity"
        )
        return Response({"sessions": list(sessions)})


class SessionRevokeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        session = UserSession.objects.filter(
            id=session_id, user=request.user
        ).first()

        if not session:
            return Response(
                {"error": "Session not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        session.delete()

        SecurityEvent.log_event(
            "session_terminated",
            request,
            user=request.user,
            description=f"Session {session_id} revoked",
        )

        return Response({"detail": "Session revoked"})
