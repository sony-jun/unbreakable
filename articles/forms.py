from django import forms
from .models import Articles, Comment
from django.forms import Select, FileInput


class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = [
            "content",
            "picture",
            "disclosure",
            "feelings",
            "music_url",
            "music_start",
        ]
        labels = {
            "content": "내용",
            "picture": "이미지",
            "disclosure": "공개여부",
            "feelings": "감정표현",
            "music_url": "유튜브URL",
            "music_start": "시작지점(초)",
        }
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "border border-2 border-dark rounded-1 mx-1",
                    "style": "background: transparent;",
                    "placeholder": "리뷰를 입력해주세요",
                }
            ),
            "feelings": Select(
                attrs={
                    "style": "background: transparent;",
                }
            ),
            "picture": FileInput(
                attrs={
                    "style": "background: transparent;",
                }
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 2,
                    "style": "background: transparent;",
                    "class": "border border-2 border-dark bg-white rounded-1 text-dark p-3 font-space shadow-sm scroll-none",
                }
            ),
        }

        labels = {
            "content": "",
        }
