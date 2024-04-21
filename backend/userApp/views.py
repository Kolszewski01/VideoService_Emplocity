from django.shortcuts import render, redirect
from .forms import MyUserRegistrationForm, AvatarChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView as DefaultLogoutView
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.views.generic import FormView
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from video.models import Video
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


def register(request):
    if request.method == "POST":
        form = MyUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Aktywuj swoje konto.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(mail_subject, message, 'popocompany53@gmail.com', [user.email], fail_silently=False)
            return redirect('account_activation_sent')
    else:
        form = MyUserRegistrationForm()
    return render(request, 'register.html', {'form': form})

UserModel = get_user_model()

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return redirect('login')
    else:
        return render(request, 'activation_invalid.html')

class ChangeAvatarView(FormView):
    template_name = 'change_avatar.html'
    form_class = AvatarChangeForm
    success_url = reverse_lazy('all_videos')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

class LogoutView(DefaultLogoutView):
    next_page = reverse_lazy('main')
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


class MyVideosView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        user_videos = Video.objects.filter(author=request.user)
        return render(request, 'my_videos.html', {'user_videos': user_videos})


class LikedVideosView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        liked_videos = request.user.liked_videos.all()
        return render(request, 'liked_videos.html', {'liked_videos': liked_videos})
