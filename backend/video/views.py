from django.shortcuts import render
from .models import Video


def all_videos(request):
    videos = Video.objects.all()
    return render(request, 'all_videos.html', {'videos': videos})