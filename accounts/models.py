from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    birthday = models.DateField(null=True) # null=True 조건을 빼야하는데 소셜 로그인 이슈로 일단 추가
    phone_number = models.CharField(max_length=15)
    fullname = models.CharField(max_length=30)