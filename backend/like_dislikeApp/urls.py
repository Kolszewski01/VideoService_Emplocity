from django.urls import path
from . import views

urlpatterns = [
    path('video/<uuid:video_id>/like/', views.like_or_dislike_video, {'like': True}, name='like_video'),
    path('video/<uuid:video_id>/dislike/', views.like_or_dislike_video, {'like': False}, name='dislike_video'),
]
