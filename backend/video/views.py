import uuid
from django.shortcuts import render, get_object_or_404
from .models import Video
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404

def all_videos(request):
    video_list = Video.objects.all()
    paginator = Paginator(video_list, 10)
    page_number = request.GET.get('page', 1)
    try:
        videos = paginator.page(page_number)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(request, 'all_videos.html', {'videos': videos})

def video_detail(request, year=None, month=None, day=None, video=None, video_id=None):
    if video_id:
        try:
            uuid.UUID(video_id)
            video = get_object_or_404(Video, id=video_id)
        except ValueError:
            raise Http404("Nieprawidłowy format UUID")
    else:
        video = get_object_or_404(Video, slug=video, uploaded_at__year=year, uploaded_at__month=month, uploaded_at__day=day)

    video.views += 1
    video.save(update_fields=['views'])

    return render(request, 'detail.html', {'video': video})


def share_video(request, video_id):
    try:
        uuid.UUID(video_id)
        video = get_object_or_404(Video, id=video_id)
    except ValueError:
        return HttpResponse("Nieprawidłowy format UUID", status=400)

    video_url = request.build_absolute_uri(video.get_absolute_url())
    return HttpResponse(video_url)
