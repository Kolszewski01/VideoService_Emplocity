import uuid
from django.shortcuts import render, get_object_or_404, redirect
from .models import Video
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404
from django.db.models import Count
from .forms import VideoForm
from django.utils.text import slugify
from django.utils import timezone

def all_videos(request):
    video_list = Video.objects.all().order_by('-uploaded_at')
    for video in video_list:
        video.num_likes = video.likes.filter(like=True).count()
        video.num_dislikes = video.likes.filter(like=False).count()
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
            video = get_object_or_404(Video, url_path=video_id)
        except ValueError:
            raise Http404("Nieprawidłowy format UUID")
    else:
        video = get_object_or_404(Video, slug=video, uploaded_at__year=year, uploaded_at__month=month, uploaded_at__day=day)

    video_tags_ids = video.tags.values_list('id', flat=True)
    similar_videos = Video.objects.filter(tags__id__in=video_tags_ids).exclude(id=video.id)
    similar_videos = similar_videos.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]

    return render(request, 'detail.html', {'video': video, 'similar_videos': similar_videos})



def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploaded_at = timezone.now()
            video.slug = slugify(video.title)
            if request.user.is_authenticated:
                video.author = request.user

            video.save()

            tags_data = form.cleaned_data['tags']

            if isinstance(tags_data, str):
                tags_list = [tag.strip() for tag in tags_data.split(',')]
            elif isinstance(tags_data, list):
                tags_list = tags_data
            else:
                tags_list = []

            tags_list = [tag for tag in tags_list if tag]

            video.tags.set(tags_list)

            return redirect('home')
    else:
        form = VideoForm()
    return render(request, 'upload_video.html', {'form': form})
    video_url = request.build_absolute_uri(video.get_absolute_url())
    return HttpResponse(video_url)

from django.shortcuts import render
from .models import Video

def search_feature(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')
        posts = Video.objects.filter(title__icontains=search_query).distinct() | Video.objects.filter(tags__name__icontains=search_query).distinct()
        return render(request, 'search_video.html', {'query': search_query, 'posts': posts})
    else:
        return render(request, 'search_video.html', {})

@require_POST
# @csrf_exempt
def update_video_views(request, video_id):
    try:
        video = get_object_or_404(Video, url_path=video_id)
        video.views += 1
        video.save(update_fields=['views'])
        return JsonResponse({'status': 'success', 'message': 'Video view count updated.', 'views': video.views})
    except Video.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Video not found.'}, status=404)


