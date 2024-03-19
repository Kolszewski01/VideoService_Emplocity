from django.test import TestCase, Client
from django.urls import reverse
from .models import Video
from userApp.models import MyUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone


class AllVideosViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_all_videos_view_GET(self):
        response = self.client.get(reverse('all_videos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_videos.html')


class VideoDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.video = Video.objects.create(
            title='Test Video',
            video_file='test_video.mp4',
            description='Test video description'
        )

    def test_video_detail_view_GET(self):
        response = self.client.get(reverse('video_details', args=[self.video.uploaded_at.year,
                                                                self.video.uploaded_at.month,
                                                                self.video.uploaded_at.day,
                                                                self.video.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail.html')


class UploadVideoViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = MyUser.objects.create_user(username='testuser', password='testpassword', email='test@email.com')

    def test_upload_video_view_GET(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('upload_video'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload_video.html')

    def test_upload_video_view_POST_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')

        form_data = {
            'title': 'Test Video',
            'video_file': SimpleUploadedFile('test_video.mp4', b'fake video content', content_type='video/mp4'),
            'description': 'Test video description',
            'tags': 'tag1, tag2, tag3'
        }

        response = self.client.post(reverse('upload_video'), data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Video.objects.filter(title='Test Video', author=self.user).exists())

    def test_upload_video_view_POST_unauthenticated_user(self):
        self.client.logout()

        form_data = {
            'title': 'Test Video',
            'video_file': SimpleUploadedFile('test_video.mp4', b'fake video content', content_type='video/mp4'),
            'description': 'Test video description',
            'tags': 'tag1, tag2, tag3'
        }

        response = self.client.post(reverse('upload_video'), data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Video.objects.filter(title='Test Video', author=None).exists())

    def test_create_user_with_email(self):
        user = MyUser.objects.create_user(username='testuser2', password='testpassword2', email='test2@email.com')
        self.assertEqual(user.email, 'test2@email.com')
