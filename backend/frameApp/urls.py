from django.urls import path
from .views import FrameList, FrameDetail, UserFrameList, UserFrameDetail

urlpatterns = [
    path('frames/', FrameList.as_view(), name='frame-list'),
    path('frames/<int:pk>/', FrameDetail.as_view(), name='frame-detail'),
    path('userframes/', UserFrameList.as_view(), name='userframe-list'),
    path('userframes/<int:pk>/', UserFrameDetail.as_view(), name='userframe-detail'),
]
