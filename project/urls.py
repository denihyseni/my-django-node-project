"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from university.secure_auth_views import (
    SecureTokenObtainView,
    SecureTokenRefreshView,
    SecureLogoutView,
    SessionListView,
    SessionRevokeView,
)


def home(request):
    return HttpResponse(
        "<h1>University API</h1>"
        "<p>Available endpoints: <a href='/admin/'>Admin</a>, <a href='/api/university/'>API</a></p>",
        content_type='text/html'
    )

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    # Secure authentication endpoints
    path('api/auth/token/', SecureTokenObtainView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', SecureTokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/logout/', SecureLogoutView.as_view(), name='logout'),
    path('api/auth/sessions/', SessionListView.as_view(), name='session_list'),
    path('api/auth/sessions/<int:session_id>/revoke/', SessionRevokeView.as_view(), name='session_revoke'),
    path('api/university/', include('university.urls')),
]
