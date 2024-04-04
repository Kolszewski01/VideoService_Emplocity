from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Frame, UserFrame
from .serializers import FrameSerializer, UserFrameSerializer


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
