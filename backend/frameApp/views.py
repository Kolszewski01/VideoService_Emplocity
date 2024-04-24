from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Frame, UserFrame
from .serializers import FrameSerializer, UserFrameSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Frame
import requests

class FrameList(ListAPIView):
    queryset = Frame.objects.all()
    serializer_class = FrameSerializer

class FrameDetail(RetrieveAPIView):
    queryset = Frame.objects.all()
    serializer_class = FrameSerializer

class UserFrameList(ListAPIView):
    queryset = UserFrame.objects.all()
    serializer_class = UserFrameSerializer

class UserFrameDetail(RetrieveAPIView):
    queryset = UserFrame.objects.all()
    serializer_class = UserFrameSerializer


def list_frames(request):
    frames = Frame.objects.all()
    return render(request, 'buy_frame.html', {'frames': frames})
