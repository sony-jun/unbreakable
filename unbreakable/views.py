from django.shortcuts import render
from articles.models import Articles

def main(request):
    articles = Articles.objects.filter(user=request.user.pk)
    context = {
        'articles':articles,
    }
    return render(request, 'main.html', context)