from django.urls import path
from .views import all_videos, video_detail, upload_video, search_feature, update_video_views, add_comment
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('videos/<uuid:video_id>/', views.video_detail, name='video_details_by_id'),
    path('all-videos/', all_videos, name='all_videos'),
    path('<int:year>/<int:month>/<int:day>/<slug:video>', video_detail, name='video_details'),
    path('videos/<uuid:video_id>/', video_detail, name='video_details_by_id'),
    path('upload/', upload_video, name='upload_video'),
    path('search/', search_feature, name='search_feature'),
    path('add_comment/<uuid:video_id>/', add_comment, name='add_comment'),
    path('add_comment/<uuid:video_id>/<int:parent_comment_id>/', add_comment, name='reply_comment'),
    path('update_views/<uuid:video_id>/', update_video_views, name='update_video_views'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
