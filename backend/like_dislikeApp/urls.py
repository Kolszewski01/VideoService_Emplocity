from django.urls import path
from . import views

urlpatterns = [
    path('video/<uuid:video_id>/like/', views.like_or_dislike_video, {'like': True}, name='like_video'),
    path('video/<uuid:video_id>/dislike/', views.like_or_dislike_video, {'like': False}, name='dislike_video'),
    path('comment/<int:comment_id>/like/', views.like_or_dislike_comment, {'like': True}, name='like_comment'),
    path('comment/<int:comment_id>/dislike/', views.like_or_dislike_comment, {'like': False}, name='dislike_comment'),
    path('liked-videos/', views.UserLikedVideosListView.as_view(), name='liked_videos'),

]
