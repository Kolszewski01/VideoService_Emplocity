from django.test import TestCase
from .models import MyUser


class MyUserTestCase(TestCase):
    def setUp(self):
        MyUser.objects.create_user(email='test@test.com', username='TestUser', password='password123')

    def test_user_creation(self):
        user = MyUser.objects.get(email='test@test.com')
        self.assertEqual(user.username, 'TestUser')




