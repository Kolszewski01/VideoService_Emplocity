from django.db import models
import uuid
from django.urls import reverse
from django.conf import settings
from taggit.managers import TaggableManager




class Video(models.Model):
    class Type(models.TextChoices):
        PUBLIC = 'PB', 'Public'
        PRIVATE = 'PR', 'Private'

    url_path = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique_for_date='uploaded_at')
    video_file = models.FileField(upload_to='videos/')
    description = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='my_videos',
        null=True,
        blank=True
    )
    type = models.CharField(max_length=2, choices=Type.choices, default=Type.PUBLIC)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    tags = TaggableManager()
    objects = models.Manager()
    thumbnail = models.ImageField(upload_to='video_thumbnails/', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('video_details', args=[self.uploaded_at.year,
                                              self.uploaded_at.month,
                                              self.uploaded_at.day,
                                              self.slug])
