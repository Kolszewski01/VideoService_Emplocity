from django.test import TestCase
from frameApp.models import Frame, UserFrame
from userApp.models import MyUser
from frameApp.serializers import FrameSerializer, UserFrameSerializer


class FrameTestCase(TestCase):
    def setUp(self):
        self.frame = Frame.objects.create(frame_name="Test Frame", frame_url="http://example.com")

    def test_frame_creation(self):
        self.assertEqual(self.frame.frame_name, "Test Frame")
        self.assertEqual(self.frame.frame_url, "http://example.com")


class UserFrameTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(email='test@test.com', username='TestUser', password='password123')
        self.frame = Frame.objects.create(frame_name="User Frame", frame_url="http://example.com/frame")
        self.user_frame = UserFrame.objects.create(user=self.user, frame=self.frame)

    def test_user_frame_creation(self):
        self.assertEqual(self.user_frame.user, self.user)
        self.assertEqual(self.user_frame.frame, self.frame)
        self.assertEqual(str(self.user_frame), f'{self.user.username} - {self.frame.frame_name}')


class FrameSerializerTest(TestCase):
    def setUp(self):
        self.frame_attributes = {
            'frame_name': 'Test Frame',
            'frame_url': 'http://example.com/frame',
        }
        self.frame = Frame.objects.create(**self.frame_attributes)
        self.serializer = FrameSerializer(instance=self.frame)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'frame_name', 'frame_url']))

    def test_frame_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['frame_name'], self.frame_attributes['frame_name'])


class UserFrameSerializerTest(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        self.frame = Frame.objects.create(frame_name='Test Frame', frame_url='http://example.com/frame')
        self.user_frame = UserFrame.objects.create(user=self.user, frame=self.frame)
        self.serializer = UserFrameSerializer(instance=self.user_frame)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'user', 'frame']))

    def test_user_field_content(self):
        data = self.serializer.data
        # Używam 'id_user' jako identyfikatora użytkownika
        self.assertEqual(data['user'], self.user.id_user)

    def test_frame_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['frame'], self.frame.id)
