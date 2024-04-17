from rest_framework import generics
from .models import FaceChat
from .serializers import FaceChatSerializer


class FaceChatList(generics.ListAPIView):
    queryset = FaceChat.objects.all()
    serializer_class = FaceChatSerializer


# 세부내역 조회
class FaceChatDetailView(generics.RetrieveAPIView):
    queryset = FaceChat.objects.all()
    serializer_class = FaceChatSerializer


# 생성
class FaceChatCreate(generics.ListCreateAPIView):
    queryset = FaceChat.objects.all()
    serializer_class = FaceChatSerializer
