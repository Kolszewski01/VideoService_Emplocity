from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from video.models import Video, Comment
from .models import Like, CommentLike
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


@login_required
def like_or_dislike_video(request, video_id, like=True):
    video = get_object_or_404(Video, url_path=video_id)
    Like.objects.update_or_create(user=request.user, video=video, defaults={'like': like})

    num_likes = video.likes.filter(like=True).count()
    num_dislikes = video.likes.filter(like=False).count()

    return JsonResponse({'num_likes': num_likes, 'num_dislikes': num_dislikes})


@login_required
def like_or_dislike_comment(request, comment_id, like=True):
    comment = get_object_or_404(Comment, id=comment_id)
    CommentLike.objects.update_or_create(user=request.user, comment=comment, defaults={'like': like})

    num_likes = comment.likes.filter(like=True).count()
    num_dislikes = comment.likes.filter(like=False).count()

    return JsonResponse({'num_likes': num_likes, 'num_dislikes': num_dislikes})

class UserLikedVideosListView(LoginRequiredMixin, ListView):
    model = Like
    template_name = 'liked_videos.html'
    context_object_name = 'liked_videos'

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user, like=True)