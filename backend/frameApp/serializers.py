from rest_framework import serializers
from .models import Frame, UserFrame

class FrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = '__all__'

class UserFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFrame
        fields = '__all__'
