from django.db import models
from django.conf import settings
from video.models import Comment

class CommentLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'comment')

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey('video.Video', on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'video')


