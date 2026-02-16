from django.db import models
from django.contrib.auth.models import User
from djongo import models as djongo_models


class UserProfile(models.Model):
    """Extended user profile for fitness tracking"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    fitness_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='beginner'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        db_table = 'users'


class Team(djongo_models.Model):
    """Team model for group fitness challenges"""
    _id = djongo_models.ObjectIdField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_teams')
    members = models.ManyToManyField(User, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'teams'


class Activity(djongo_models.Model):
    """Activity model for logging fitness activities"""
    _id = djongo_models.ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(
        max_length=50,
        choices=[
            ('running', 'Running'),
            ('walking', 'Walking'),
            ('cycling', 'Cycling'),
            ('swimming', 'Swimming'),
            ('gym', 'Gym Workout'),
            ('yoga', 'Yoga'),
            ('sports', 'Sports'),
            ('other', 'Other'),
        ],
        default='other'
    )
    duration_minutes = models.IntegerField()
    distance_km = models.FloatField(blank=True, null=True)
    calories_burned = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    activity_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"

    class Meta:
        db_table = 'activities'


class Leaderboard(djongo_models.Model):
    """Leaderboard model for competitive tracking"""
    _id = djongo_models.ObjectIdField()
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='leaderboard')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboard_entries')
    total_activities = models.IntegerField(default=0)
    total_calories = models.IntegerField(default=0)
    total_distance = models.FloatField(default=0.0)
    total_duration_minutes = models.IntegerField(default=0)
    rank = models.IntegerField()
    points = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rank {self.rank} - {self.user.username}"

    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']


class Workout(djongo_models.Model):
    """Workout suggestions model"""
    _id = djongo_models.ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_suggestions')
    fitness_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ]
    )
    workout_type = models.CharField(
        max_length=50,
        choices=[
            ('cardio', 'Cardio'),
            ('strength', 'Strength'),
            ('flexibility', 'Flexibility'),
            ('balance', 'Balance'),
            ('endurance', 'Endurance'),
        ]
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration_minutes = models.IntegerField()
    exercises = models.JSONField(default=list)
    difficulty_rating = models.IntegerField(default=5)  # 1-10 scale
    suggested_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    class Meta:
        db_table = 'workouts'
