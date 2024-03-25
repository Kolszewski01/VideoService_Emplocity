from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from video.models import Video
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Like


@login_required
def like_or_dislike_video(request, video_id, like=True):
    video = get_object_or_404(Video, url_path=video_id)
    Like.objects.update_or_create(user=request.user, video=video, defaults={'like': like})

    num_likes = video.likes.filter(like=True).count()
    num_dislikes = video.likes.filter(like=False).count()

    return JsonResponse({'num_likes': num_likes, 'num_dislikes': num_dislikes})
