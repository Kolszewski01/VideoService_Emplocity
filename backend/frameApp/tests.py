from django.test import TestCase
from .models import Frame, UserFrame
from userApp.models import MyUser

class FrameTestCase(TestCase):
    def setUp(self):
        # Tworzenie ramki
        self.frame = Frame.objects.create(frame_name="Test Frame", frame_url="http://example.com")

    def test_frame_creation(self):
        # Testowanie, czy ramka została poprawnie utworzona
        self.assertEqual(self.frame.frame_name, "Test Frame")
        self.assertEqual(self.frame.frame_url, "http://example.com")

class UserFrameTestCase(TestCase):
    def setUp(self):
        # Tworzenie użytkownika
        self.user = MyUser.objects.create_user(email='test@test.com', username='TestUser', password='password123')
        # Tworzenie ramki
        self.frame = Frame.objects.create(frame_name="User Frame", frame_url="http://example.com/frame")
        # Tworzenie relacji użytkownik-ramka
        self.user_frame = UserFrame.objects.create(user=self.user, frame=self.frame)

    def test_user_frame_creation(self):
        # Testowanie, czy relacja użytkownik-ramka została poprawnie utworzona
        self.assertEqual(self.user_frame.user, self.user)
        self.assertEqual(self.user_frame.frame, self.frame)
        self.assertEqual(str(self.user_frame), f'{self.user.username} - {self.frame.frame_name}')
