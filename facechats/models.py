from django.conf import settings
from django.db import models
from posts.models import Tag

class FaceChat(models.Model):
    # face_chat_id = models.AutoField(primary_key=True) # id값은 기본적으로 자동으로 생성, 사용자 정의로 필드명을 선언할땐 이렇게 작성하고 이런 경우 자동으로 id는 생성되지x
    room_name = models.CharField(max_length=255)
    host_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hosted_chats')
    stauts = models.IntegerField(default=0)  # 0: 진행 중, 1: 종료, 2: 중지
    count = models.IntegerField(default=0) # 조회 수
    max_participants = models.IntegerField(default=4) # 최대 인원 설정
    current_participants = models.IntegerField(default=0) # 현재 인원 설정
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(auto_now=True)

# History Table 
class FaceChatParticipant(models.Model):
    face_chat_id = models.ForeignKey(FaceChat, on_delete=models.CASCADE, related_name='participants')
    seqno = models.IntegerField() # 자동 증가
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participated_chats')
    joined_at = models.DateTimeField(auto_now_add=True)
    exited_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ('face_chat_id', 'seqno')


class FaceChatTag(models.Model):
    face_chat_id = models.ForeignKey('FaceChat', on_delete=models.CASCADE, related_name='tags')
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='facechats')

    class Meta:
        unique_together = ('face_chat_id', 'tag_id')