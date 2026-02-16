from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'profile_picture', 'fitness_level', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    _id = serializers.CharField(source='_id', read_only=True)
    owner = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['_id', 'name', 'description', 'owner', 'members', 'created_at', 'updated_at']
        read_only_fields = ['_id', 'created_at', 'updated_at', 'owner']


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    _id = serializers.CharField(source='_id', read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Activity
        fields = ['_id', 'user', 'activity_type', 'duration_minutes', 'distance_km', 
                  'calories_burned', 'description', 'activity_date', 'created_at', 'updated_at']
        read_only_fields = ['_id', 'created_at', 'updated_at', 'user']


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    _id = serializers.CharField(source='_id', read_only=True)
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)

    class Meta:
        model = Leaderboard
        fields = ['_id', 'team', 'user', 'total_activities', 'total_calories', 
                  'total_distance', 'total_duration_minutes', 'rank', 'points', 'updated_at']
        read_only_fields = ['_id', 'updated_at']


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for Workout model"""
    _id = serializers.CharField(source='_id', read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Workout
        fields = ['_id', 'user', 'fitness_level', 'workout_type', 'title', 'description',
                  'duration_minutes', 'exercises', 'difficulty_rating', 'suggested_date',
                  'is_completed', 'created_at', 'updated_at']
        read_only_fields = ['_id', 'created_at', 'updated_at', 'user']
