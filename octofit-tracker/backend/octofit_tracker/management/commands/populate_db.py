from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from octofit_tracker.models import UserProfile, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete existing data
        UserProfile.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().exclude(is_superuser=True).delete()

        # Create users (super heroes)
        marvel_heroes = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'first_name': 'Tony', 'last_name': 'Stark'},
            {'username': 'captainamerica', 'email': 'cap@marvel.com', 'first_name': 'Steve', 'last_name': 'Rogers'},
            {'username': 'blackwidow', 'email': 'widow@marvel.com', 'first_name': 'Natasha', 'last_name': 'Romanoff'},
        ]
        dc_heroes = [
            {'username': 'batman', 'email': 'batman@dc.com', 'first_name': 'Bruce', 'last_name': 'Wayne'},
            {'username': 'superman', 'email': 'superman@dc.com', 'first_name': 'Clark', 'last_name': 'Kent'},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com', 'first_name': 'Diana', 'last_name': 'Prince'},
        ]

        marvel_users = [User.objects.create_user(**hero) for hero in marvel_heroes]
        dc_users = [User.objects.create_user(**hero) for hero in dc_heroes]

        # Create profiles
        for user in marvel_users + dc_users:
            UserProfile.objects.create(user=user, fitness_level='beginner')

        # Create teams
        marvel_team = Team.objects.create(name='Team Marvel', description='Marvel Super Heroes', owner=marvel_users[0])
        dc_team = Team.objects.create(name='Team DC', description='DC Super Heroes', owner=dc_users[0])
        marvel_team.members.set(marvel_users)
        dc_team.members.set(dc_users)

        # Create activities
        for user in marvel_users:
            Activity.objects.create(
                user=user,
                activity_type='running',
                duration_minutes=30,
                distance_km=5.0,
                calories_burned=300,
                description='Morning run',
                activity_date=datetime.now()
            )
        for user in dc_users:
            Activity.objects.create(
                user=user,
                activity_type='cycling',
                duration_minutes=45,
                distance_km=15.0,
                calories_burned=500,
                description='Evening ride',
                activity_date=datetime.now()
            )

        # Create workouts
        for user in marvel_users + dc_users:
            Workout.objects.create(
                user=user,
                fitness_level='beginner',
                workout_type='cardio',
                title='Hero Cardio',
                description='Superhero cardio workout',
                duration_minutes=40,
                exercises=['Warm-up', 'Cardio', 'Cool-down'],
                difficulty_rating=7,
                suggested_date=datetime.now() + timedelta(days=1)
            )

        # Create leaderboard entries
        for idx, user in enumerate(marvel_users + dc_users, start=1):
            Leaderboard.objects.create(
                team=marvel_team if user in marvel_users else dc_team,
                user=user,
                total_activities=1,
                total_calories=300 if user in marvel_users else 500,
                total_distance=5.0 if user in marvel_users else 15.0,
                total_duration_minutes=30 if user in marvel_users else 45,
                rank=idx,
                points=100 * idx
            )

        self.stdout.write(self.style.SUCCESS('Database populated with test data!'))