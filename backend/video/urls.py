from django.urls import path
from .views import all_videos

urlpatterns = [
    path('all-videos/', all_videos, name='all_videos'),
]