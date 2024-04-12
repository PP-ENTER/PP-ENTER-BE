from django.conf import settings
from django.db import models
from posts.models import Tag

class FaceChat(models.Model):
    # face_chat_id = models.AutoField(primary_key=True) # id값은 기본적으로 자동으로 생성, 사용자 정의로 필드명을 선언할땐 이렇게 작성하고 이런 경우 자동으로 id는 생성되지x
    room_name = models.CharField(max_length=255)
    host_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hosted_chats')
    stauts = models.IntegerField()  # 0: 진행 중, 1: 종료, 2: 중지 -> boolena type 
    duration = models.DateTimeField()  # 날짜
    count = models.IntegerField() # 조회 수
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FaceChatParticipant(models.Model):
    face_chat_id = models.ForeignKey(FaceChat, on_delete=models.CASCADE, related_name='participants')
    seqno = models.IntegerField() # 자동증가, 최대 4
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participated_chats')
    joined_at = models.DateTimeField()

    class Meta:
        unique_together = ('face_chat_id', 'seqno')


class FaceChatTag(models.Model):
    face_chat_id = models.ForeignKey('FaceChat', on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='facechats')

    class Meta:
        unique_together = ('face_chat_id', 'tag')