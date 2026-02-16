from django.contrib import admin
from .models import UserProfile, Team, Activity, Leaderboard, Workout


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile"""
    list_display = ('user', 'fitness_level', 'created_at', 'updated_at')
    list_filter = ('fitness_level', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team"""
    list_display = ('name', 'owner', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'owner__username')
    filter_horizontal = ('members',)
    readonly_fields = ('created_at', 'updated_at', '_id')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity"""
    list_display = ('user', 'activity_type', 'duration_minutes', 'calories_burned', 'activity_date')
    list_filter = ('activity_type', 'activity_date', 'created_at')
    search_fields = ('user__username', 'description')
    readonly_fields = ('created_at', 'updated_at', '_id')


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard"""
    list_display = ('rank', 'user', 'team', 'total_activities', 'points')
    list_filter = ('rank', 'team', 'updated_at')
    search_fields = ('user__username', 'team__name')
    readonly_fields = ('updated_at', '_id')
    ordering = ('rank',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin interface for Workout"""
    list_display = ('title', 'user', 'fitness_level', 'workout_type', 'is_completed', 'suggested_date')
    list_filter = ('fitness_level', 'workout_type', 'is_completed', 'suggested_date')
    search_fields = ('title', 'user__username', 'description')
    readonly_fields = ('created_at', 'updated_at', '_id')
