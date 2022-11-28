from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticlesForm
from django.contrib import messages

# Create your views here.
from .models import Articles
from django.contrib.auth.decorators import login_required


def articles_index(request):
    articles = Articles.objects.all()
    context = {
        "articles": articles,
    }
    return render(request, "articles/articles_index.html", context)


# @login_required
def articles_create(request):
    if request.method == "POST":
        articles_form = ArticlesForm(request.POST, request.FILES)
        if articles_form.is_valid():
            articles = articles_form.save(commit=False)
            articles.user = request.user
            articles.save()
            return redirect("articles:articles_index")  # 수정 할 예정임(어디로 보낼까?)
    else:
        articles_form = ArticlesForm()
    context = {
        "articles_form": articles_form,
    }
    return render(request, "articles/articles_create.html", context)


def articles_detail(request, articles_pk):
    articles = get_object_or_404(Articles, pk=articles_pk)
    context = {
        "articles": articles,
    }
    return render(request, "articles/articles_detail.html", context)


# @login_required
def articles_delete(request, articles_pk):
    articles = get_object_or_404(Articles, pk=articles_pk)
    if request.user == articles.user:
        if request.method == "POST":
            articles.delete()
            return redirect("articles:articles_index", articles_pk)  # 아마도 메인페이지?
    return redirect("articles:articles_detail", articles_pk)


# @login_required
def articles_update(request, articles_pk):
    articles = get_object_or_404(Articles, pk=articles_pk)
    if request.user == articles.user:
        if request.method == "POST":
            articles_form = ArticlesForm(request.POST, request.FILES, instance=articles)
            if articles_form.is_valid():
                form = articles_form.save(commit=False)
                form.user = request.user
                form.save()
            return redirect("articles:articles_detail", articles_pk)
        else:
            articles_form = ArticlesForm(instance=articles)
        context = {
            "articles_form": articles_form,
        }
        return render(request, "articles/articles_update.html", context)
    else:
        messages.warning(request, "작성자만 수정 할 수 있습니다.")
        return redirect("articles:articles_index")
