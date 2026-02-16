from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import UserProfile, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta


class UserProfileTestCase(TestCase):
    """Test cases for UserProfile model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            fitness_level='beginner'
        )

    def test_user_profile_creation(self):
        """Test user profile creation"""
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.fitness_level, 'beginner')

    def test_user_profile_str(self):
        """Test user profile string representation"""
        self.assertEqual(str(self.profile), "testuser's Profile")


class TeamTestCase(TestCase):
    """Test cases for Team model"""

    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='testpass123'
        )
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team',
            owner=self.owner
        )
        self.member = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='testpass123'
        )

    def test_team_creation(self):
        """Test team creation"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.owner.username, 'owner')

    def test_add_team_member(self):
        """Test adding member to team"""
        self.team.members.add(self.member)
        self.assertIn(self.member, self.team.members.all())

    def test_team_str(self):
        """Test team string representation"""
        self.assertEqual(str(self.team), 'Test Team')


class ActivityTestCase(TestCase):
    """Test cases for Activity model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration_minutes=30,
            distance_km=5.0,
            calories_burned=300,
            activity_date=datetime.now()
        )

    def test_activity_creation(self):
        """Test activity creation"""
        self.assertEqual(self.activity.activity_type, 'running')
        self.assertEqual(self.activity.duration_minutes, 30)

    def test_activity_str(self):
        """Test activity string representation"""
        self.assertIn('testuser', str(self.activity))
        self.assertIn('running', str(self.activity))


class WorkoutTestCase(TestCase):
    """Test cases for Workout model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.workout = Workout.objects.create(
            user=self.user,
            fitness_level='beginner',
            workout_type='cardio',
            title='Morning Run',
            description='Easy morning run',
            duration_minutes=30,
            exercises=['Warm-up', 'Running', 'Cool-down'],
            suggested_date=datetime.now() + timedelta(days=1)
        )

    def test_workout_creation(self):
        """Test workout creation"""
        self.assertEqual(self.workout.title, 'Morning Run')
        self.assertFalse(self.workout.is_completed)

    def test_mark_workout_complete(self):
        """Test marking workout as complete"""
        self.workout.is_completed = True
        self.workout.save()
        self.assertTrue(self.workout.is_completed)

    def test_workout_str(self):
        """Test workout string representation"""
        self.assertIn('Morning Run', str(self.workout))


class APITestCase(APITestCase):
    """API test cases for all viewsets"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            fitness_level='beginner'
        )

    def test_user_list_api(self):
        """Test user list API endpoint"""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activity_create_api(self):
        """Test activity creation via API"""
        self.client.force_authenticate(user=self.user)
        data = {
            'activity_type': 'running',
            'duration_minutes': 30,
            'distance_km': 5.0,
            'calories_burned': 300,
            'activity_date': datetime.now().isoformat()
        }
        response = self.client.post('/api/activities/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_team_create_api(self):
        """Test team creation via API"""
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'Test Team',
            'description': 'A test team'
        }
        response = self.client.post('/api/teams/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthenticated_access_denied(self):
        """Test that unauthenticated users cannot create resources"""
        data = {
            'activity_type': 'running',
            'duration_minutes': 30,
            'activity_date': datetime.now().isoformat()
        }
        response = self.client.post('/api/activities/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
