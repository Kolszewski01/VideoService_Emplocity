from django.test import TestCase
from .models import MyUser
from .serializers import MyUserSerializer


class MyUserTestCase(TestCase):
    def setUp(self):
        MyUser.objects.create_user(email='test@test.com', username='TestUser', password='password123')

    def test_user_creation(self):
        user = MyUser.objects.get(email='test@test.com')
        self.assertEqual(user.username, 'TestUser')




class MyUserSerializerTest(TestCase):
    def setUp(self):
        self.user_attributes = {
            'username': 'testuser',
            'email': 'test@example.com',
        }
        self.user = MyUser.objects.create(**self.user_attributes)
        self.serializer = MyUserSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id_user', 'username', 'email', 'registration_date']))

    def test_username_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['username'], self.user_attributes['username'])

