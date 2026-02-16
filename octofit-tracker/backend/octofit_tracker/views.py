from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from .models import UserProfile, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, UserProfileSerializer, TeamSerializer,
    ActivitySerializer, LeaderboardSerializer, WorkoutSerializer
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for User model"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user details"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for UserProfile model"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter profiles based on user"""
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Assign current user to profile"""
        serializer.save(user=self.request.user)


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for Team model"""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Assign current user as team owner"""
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_member(self, request, pk=None):
        """Add a member to the team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            team.members.add(user)
            return Response({'status': 'member added'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_member(self, request, pk=None):
        """Remove a member from the team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            team.members.remove(user)
            return Response({'status': 'member removed'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for Activity model"""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter activities for current user"""
        user = self.request.user
        if self.request.query_params.get('user_id'):
            user_id = self.request.query_params.get('user_id')
            return Activity.objects.filter(user_id=user_id)
        return Activity.objects.filter(user=user)

    def perform_create(self, serializer):
        """Assign current user to activity"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get activity statistics for current user"""
        activities = self.get_queryset()
        total_activities = activities.count()
        total_calories = sum(a.calories_burned or 0 for a in activities)
        total_distance = sum(a.distance_km or 0 for a in activities)
        total_duration = sum(a.duration_minutes for a in activities)

        return Response({
            'total_activities': total_activities,
            'total_calories': total_calories,
            'total_distance': total_distance,
            'total_duration_minutes': total_duration,
        })


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Leaderboard model"""
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Filter leaderboard by team"""
        team_id = self.request.query_params.get('team_id')
        if team_id:
            return Leaderboard.objects.filter(team_id=team_id).order_by('rank')
        return Leaderboard.objects.all().order_by('rank')

    @action(detail=False, methods=['get'])
    def top_performers(self, request):
        """Get top 10 performers"""
        leaderboard = Leaderboard.objects.all().order_by('rank')[:10]
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ModelViewSet):
    """ViewSet for Workout model"""
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter workouts for current user"""
        user = self.request.user
        if self.request.query_params.get('completed'):
            completed = self.request.query_params.get('completed').lower() == 'true'
            return Workout.objects.filter(user=user, is_completed=completed)
        return Workout.objects.filter(user=user)

    def perform_create(self, serializer):
        """Assign current user to workout"""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_complete(self, request, pk=None):
        """Mark a workout as completed"""
        workout = self.get_object()
        workout.is_completed = True
        workout.save()
        serializer = self.get_serializer(workout)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def suggestions(self, request):
        """Get personalized workout suggestions for current user"""
        try:
            profile = request.user.profile
            fitness_level = profile.fitness_level
            workouts = Workout.objects.filter(
                user=request.user,
                fitness_level=fitness_level,
                is_completed=False
            ).order_by('suggested_date')
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
