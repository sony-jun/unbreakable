from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from articles.models import Articles
from music.models import Song
# Create your models here.
class User(AbstractUser):
    birthday = models.DateField(null=True, blank=True) # null=True 조건을 빼야하는데 소셜 로그인 이슈로 일단 추가
    phone_number = models.CharField(max_length=15)
    fullname = models.CharField(max_length=30)
    
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='re_sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    articles = models.ForeignKey(Articles, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    song = models.ForeignKey(Song, on_delete=models.SET_NULL, null=True)
    
    
class MessageDeclaration(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="message_reporter")
    reported = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message_writer')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    
    class Meta:
        constraints = [
        models.UniqueConstraint(
            fields=["reporter", "message"], name="only_one_report3"
        )
    ]
