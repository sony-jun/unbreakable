from django.shortcuts import render
from articles.models import Articles
from music.models import Song

def main(request):
    articles = Articles.objects.filter(disclosure=1)
    context = {
        'articles':articles,
    }
    return render(request, 'main.html', context)