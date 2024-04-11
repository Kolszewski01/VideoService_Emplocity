import uuid
from django.views.generic.edit import CreateView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Video, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404, JsonResponse
from django.db.models import Count, Q
from .forms import VideoForm
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

"""" Widok do ładowania wszystkich publicznych plików Video z sortowanie"""
def all_videos(request):
    sort_by = request.GET.get('sort_by')
    sort_order = request.GET.get('sort_order')

    if sort_by == 'uploaded_at':
        if sort_order == 'asc':
            video_list = Video.objects.filter(type=Video.Type.PUBLIC).order_by('uploaded_at')
        else:
            video_list = Video.objects.filter(type=Video.Type.PUBLIC).order_by('-uploaded_at')
    elif sort_by == 'views':
        if sort_order == 'asc':
            video_list = Video.objects.filter(type=Video.Type.PUBLIC).order_by('views')
        else:
            video_list = Video.objects.filter(type=Video.Type.PUBLIC).order_by('-views')
    elif sort_by == 'likes':
        if sort_order == 'asc':
            video_list = Video.objects.filter(type=Video.Type.PUBLIC).annotate(num_likes=Count('likes', filter=Q(likes=True))).order_by('num_likes')
        else:
            video_list = Video.objects.filter(type=Video.Type.PUBLIC).annotate(num_likes=Count('likes', filter=Q(likes=True))).order_by('-num_likes')
    else:
        video_list = Video.objects.filter(type=Video.Type.PUBLIC).order_by('-uploaded_at')

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
        video = get_object_or_404(Video, slug=video, uploaded_at__year=year, uploaded_at__month=month,
                                  uploaded_at__day=day)

    video.save(update_fields=['views'])
    video_tags_ids = video.tags.values_list('id', flat=True)
    similar_videos = Video.objects.filter(tags__id__in=video_tags_ids).exclude(id=video.id)
    similar_videos = similar_videos.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]
    comments = video.comments.all()

    return render(request, 'detail.html', {'video': video,
                                           'similar_videos': similar_videos,
                                           'comments': comments})



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

            return redirect('all_videos')
    else:
        form = VideoForm()
    return render(request, 'upload_video.html', {'form': form})
    video_url = request.build_absolute_uri(video.get_absolute_url())
    return HttpResponse(video_url)


def search_feature(request):
    # Check if the request is a post request.
    if request.method == 'POST':
        # Retrieve the search query entered by the user
        search_query = request.POST['search_query']
        # Filter your model by the search query
        posts = Model.objects.filter(title__contains=search_query)
        posts += Model.objects.filter(tags__contains=search_query)
        return render(request, 'base.html', {'query':search_query, 'posts':posts})
    else:
        return render(request, 'base.html',{})

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


@login_required
def add_comment(request, video_id):
    video = get_object_or_404(Video, url_path=video_id)
    parent_comment_id = request.POST.get('parent_id')
    parent_comment = None

    if parent_comment_id:
        parent_comment = get_object_or_404(Comment, id=parent_comment_id)
        if parent_comment.parent is not None:
            parent_comment = None

    if request.method == 'POST':
        content = request.POST.get('content', '')
        if content:
            Comment.objects.create(
                video=video,
                author=request.user,
                content=content,
                parent=parent_comment
            )
            return redirect('video_details_by_id', video_id=video.url_path)

    return redirect('video_details_by_id', video_id=video.url_path)




@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author == request.user:
        comment.delete()
        return JsonResponse({'status': 'success', 'message': 'Komentarz został usunięty.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Nie masz uprawnień do usunięcia tego komentarza.'}, status=403)
