from django.urls import path
from .views import all_videos, video_detail, upload_video
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('all-videos/', all_videos, name='all_videos'),
    path('<int:year>/<int:month>/<int:day>/<slug:video>', video_detail, name='video_details'),
    path('videos/<uuid:video_id>/', video_detail, name='video_details_by_id'),
    path('upload/', upload_video, name='upload_video'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)