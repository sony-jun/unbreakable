from django import forms
from .models import Song

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = [
            'song_title',
            'song_url',
            'song_thumbnail',
        ]
        labels = {
            'song_title' : '제목',
            'song_thumbnail' : '이미지',
            'song_url' : 'url',
        }