from django.urls import path
from .views import register, activate_account, account_activation_sent, ChangeAvatarView, MyVideosView, LikedVideosView
from backend.views import home

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', home, name='home'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='send-link.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),  # Poprawione
    path('account_activation_sent/', account_activation_sent, name='account_activation_sent'),
    path('change-avatar/', ChangeAvatarView.as_view(), name='change_avatar'),
    path('my_videos/', MyVideosView.as_view(), name='my_videos'),
    path('liked_videos/', LikedVideosView.as_view(), name='liked_videos'),
]
