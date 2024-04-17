from django.test import TestCase
from django.contrib.auth import get_user_model
from video.models import Video, Comment
from .models import CommentLike, Like

User = get_user_model()

class CommentLikeModelTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(email='adnrzejuuu@wp.pl',username='user1', password='test12345')
        self.user2 = User.objects.create_user(email='jakcinaimieclea@wp.pl',username='user2', password='test12345')
        self.video = Video.objects.create(title='Test Video', description='Test Description', author=self.user1)
        self.comment = Comment.objects.create(author=self.user1, video=self.video, content='Test Comment')

    def test_comment_like_creation(self):
        comment_like = CommentLike.objects.create(user=self.user1, comment=self.comment)
        self.assertEqual(comment_like.user, self.user1)
        self.assertEqual(comment_like.comment, self.comment)
        self.assertTrue(comment_like.like)

    def test_comment_like_uniqueness(self):
        CommentLike.objects.create(user=self.user1, comment=self.comment)
        with self.assertRaises(Exception):
            CommentLike.objects.create(user=self.user1, comment=self.comment)

class LikeModelTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='email@wp.pl', password='test12345')
        self.user2 = User.objects.create_user(username='user2',email='email@onet.pl', password='test12345')
        self.video = Video.objects.create(title='Test Video', description='Test Description', author=self.user1)

    def test_video_like_creation(self):
        video_like = Like.objects.create(user=self.user1, video=self.video)
        self.assertEqual(video_like.user, self.user1)
        self.assertEqual(video_like.video, self.video)
        self.assertTrue(video_like.like)

    def test_video_like_uniqueness(self):
        Like.objects.create(user=self.user1, video=self.video)
        with self.assertRaises(Exception):
            Like.objects.create(user=self.user1, video=self.video)
