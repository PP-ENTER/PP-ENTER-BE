# Generated by Django 4.2.11 on 2024-04-04 08:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('facechats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='facechattag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facechats', to='posts.tag'),
        ),
        migrations.AddField(
            model_name='facechatparticipant',
            name='face_chat_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='facechats.facechat'),
        ),
        migrations.AddField(
            model_name='facechatparticipant',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participated_chats', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facechat',
            name='host_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hosted_chats', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='facechattag',
            unique_together={('face_chat_id', 'tag')},
        ),
        migrations.AlterUniqueTogether(
            name='facechatparticipant',
            unique_together={('face_chat_id', 'seqno')},
        ),
    ]
