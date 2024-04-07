from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from .models import Video, Comment
from like_dislikeApp.models import CommentLike
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



User = get_user_model()

class CommentModelTests(TestCase):

    def setUp(self):
        # Tworzenie użytkowników
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='test12345')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='test12345')

        # Tworzenie wideo
        self.video = Video.objects.create(title='Test Video', description='Test Description', author=self.user1)

        # Tworzenie komentarzy
        self.comment1 = Comment.objects.create(video=self.video, author=self.user1, content='Pierwszy komentarz')
        self.comment2 = Comment.objects.create(video=self.video, author=self.user2, content='Drugi komentarz', parent=self.comment1)

        # Tworzenie polubień i niepolubień
        CommentLike.objects.create(user=self.user1, comment=self.comment1, like=True)
        CommentLike.objects.create(user=self.user2, comment=self.comment1, like=False)

    def test_comment_creation(self):
        self.assertEqual(self.comment1.author, self.user1)
        self.assertEqual(self.comment1.video, self.video)
        self.assertEqual(self.comment1.content, 'Pierwszy komentarz')
        self.assertIsNone(self.comment1.parent)

        # Sprawdzenie tworzenia komentarza podrzędnego
        self.assertEqual(self.comment2.parent, self.comment1)

    def test_comment_representation(self):
        self.assertTrue(str(self.comment1).startswith('Komentarz od user1 - Pierwszy komentarz'))

    def test_num_likes(self):
        # Sprawdzenie liczby polubień dla comment1
        self.assertEqual(self.comment1.num_likes(), 1)

    def test_num_dislikes(self):
        # Sprawdzenie liczby niepolubień dla comment1
        self.assertEqual(self.comment1.num_dislikes(), 1)