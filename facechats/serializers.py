from rest_framework import serializers
from .models import FaceChat

class FaceChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceChat
        
        fields = ['id', 'room_name', 'host_id', 'status', 'duration', 'count', 'created_at']
