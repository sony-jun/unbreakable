from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticlesForm, CommentForm
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from accounts.models import Message

from django.db.models.functions import Replace
from django.db.models import Value

# Create your views here.

from .models import Articles, Comment
from django.contrib.auth.decorators import login_required


def calendar_1(request):
    return render(request, "articles/calendar_1.html")


def calendar(request):
    return render(request, "articles/calendar.html")


def articles_index(request):
    articles = Articles.objects.order_by("-created_at")
    context = {
        "articles": articles,
    }
    return render(request, "articles/articles_index.html", context)


@login_required
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
        "comment_form": CommentForm(),
        "comments": articles.comment_set.all(),
    }
    return render(request, "articles/articles_detail.html", context)


@login_required
def articles_delete(request, articles_pk):
    articles = get_object_or_404(Articles, pk=articles_pk)
    if request.user == articles.user:
        if request.method == "POST":
            articles.delete()
            return redirect("articles:articles_index")  # 아마도 메인페이지?
    return redirect("articles:articles_detail", articles_pk)


@login_required
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


def comment_create(request, articles_pk):
    articles = get_object_or_404(Articles, pk=articles_pk)
    result = request.POST["parent"]

    if request.method == "POST":  # POST요청이고
        if request.user.is_authenticated:  # 로그인된 상태면
            # 댓글일 때
            if int(result) == 0:
                comment_form = CommentForm(request.POST)  # POST으로 요청온 정보를 받아서
                if comment_form.is_valid():  # 유효성 검사하고
                    comment = comment_form.save(commit=False)  # 저장 멈춰
                    # 외래키 입력
                    comment.articles = articles
                    comment.user = request.user
                    # 저장
                    comment.save()

                    context = {
                        "articles_pk": articles_pk,
                        "comment_pk": comment.pk,
                        "content": comment.content,
                        "userName": comment.user.username,
                    }
                    return JsonResponse(context)

            elif int(result) > 0:
                comment_form = CommentForm(request.POST)  # POST으로 요청온 정보를 받아서
                if comment_form.is_valid():  # 유효성 검사하고
                    comment = comment_form.save(commit=False)  # 저장 멈춰
                    # 외래키 입력
                    comment.articles = articles
                    comment.user = request.user
                    comment.parent_id = result
                    # 저장
                    comment.save()

                    context = {
                        "articles_pk": articles_pk,
                        "comment_pk": comment.pk,
                        "content": comment.content,
                        "userName": comment.user.username,
                    }
                    return JsonResponse(context)
        else:
            return HttpResponse(status=403)
    else:
        return redirect("accounts:login")


@login_required
def comment_delete(request, articles_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        if request.method == "POST":
            comment.delete()

    data = {}
    return JsonResponse(data)
