from django.urls import path
from .views import FrameList, FrameDetail, UserFrameList, UserFrameDetail, list_frames
from .payu import create_order, get_payu_token,payment_success

urlpatterns = [
    path('frames/', FrameList.as_view(), name='frame-list'),
    path('frames/<int:pk>/', FrameDetail.as_view(), name='frame-detail'),
    path('userframes/', UserFrameList.as_view(), name='userframe-list'),
    path('userframes/<int:pk>/', UserFrameDetail.as_view(), name='userframe-detail'),
    path('gif_list/', list_frames, name='gif_list'),
    path('create_order/<int:frame_id>/', create_order, name='buy_frame'),
    path('get_token/', get_payu_token, name='get_payu_token'),
    path('notify/', payment_success, name='payment-success'),

]

