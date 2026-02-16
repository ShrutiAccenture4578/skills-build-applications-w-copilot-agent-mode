"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
import os
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .views import (
    UserViewSet, UserProfileViewSet, TeamViewSet, ActivityViewSet,
    LeaderboardViewSet, WorkoutViewSet
)

# Use environment variable for codespace name
CODESPACE_NAME = os.environ.get('CODESPACE_NAME', 'localhost')

api_base_url = f"https://{CODESPACE_NAME}-8000.app.github.dev/api/"

# Create router and register viewsets
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'workouts', WorkoutViewSet, basename='workout')

# API root view
@api_view(['GET'])
def api_root(request):
    """API root endpoint"""
    return Response({
        'message': 'Welcome to OctoFit Tracker API',
        'version': '1.0.0',
        'endpoints': [
            request.build_absolute_uri('/api/users/'),
            request.build_absolute_uri('/api/profiles/'),
            request.build_absolute_uri('/api/teams/'),
            request.build_absolute_uri('/api/activities/'),
            request.build_absolute_uri('/api/leaderboard/'),
            request.build_absolute_uri('/api/workouts/'),
        ]
    }, status=200)

# Configure base URL based on environment
base_url = api_base_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
