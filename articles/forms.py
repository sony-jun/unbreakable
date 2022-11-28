from django import forms
from .models import Articles
from django.forms import Select, FileInput


class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = [
            "content",
            "picture",
            "disclosure",
            "feelings",
        ]
        labels = {
            "content": "내용",
            "picture": "이미지",
            "disclosure": "공개여부",
            "feelings": "감정표현",
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
