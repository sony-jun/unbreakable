from django.db import models
from imagekit.models import ProcessedImageField
from django.core.validators import MinValueValidator, MaxValueValidator
from imagekit.processors import ResizeToFill
from django.conf import settings
import re

from django.forms import ValidationError


with open("badwords.txt", encoding="UTF8") as file:
    CENSORED_WORDS = file.read().splitlines()


def validate_text(text):
    words = set(re.sub("[^\w]", " ", text).split())
    for censored in words:
        if censored in CENSORED_WORDS:
            raise ValidationError(f"{censored}은(는) 쓰지 말아주세요!!")


# Create your models here.
class Articles(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(validators=[validate_text])
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    picture = ProcessedImageField(
        null=True,
        upload_to="images/",
        blank=True,
        processors=[ResizeToFill(1200, 960)],
        format="JPEG",
        options={"quality": 90},
    )

    disclosure = models.BooleanField(default=True)
    # True가 공개, False가 비공개
    feelings_choices = (
        ("👿", "👿"),
        ("😞", "😞"),
        ("😊", "😊"),
    )
    feelings = models.CharField(max_length=2, choices=feelings_choices)


class Comment(models.Model):
    content = models.CharField(validators=[validate_text], max_length=160)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    articles = models.ForeignKey(Articles, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)  # 대댓글
