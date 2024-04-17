from rest_framework import serializers
from .models import FaceChat


class FaceChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceChat
        fields = [
            "id",
            "room_name",
            "host_id",
            "stauts",
            "count",
            "created_at",
            "finished_at",
        ]
