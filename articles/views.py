from django.shortcuts import render, redirect, get_object_or_404
from .forms import (
    ArticlesForm,
    CommentForm,
    ArticlesDeclarationForm,
    CommentDeclarationForm,
)
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from accounts.models import Message
from .models import Articles, Sympathy, Comment
from django.utils import timezone
from music.models import Song
from django.views.generic.base import TemplateView
import json
from django.db.models import Q
import requests
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.db.models import Value
from django.db.models.functions import Replace


def calendar(request):
    return render(request, "articles/calendar.html")


def articles_index(request):
    articles = Articles.objects.filter(disclosure=True).order_by("-created_at")
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
            so = Song.objects.filter(song_title=request.POST["song"]).exists()
            if so:
                song = Song.objects.get(song_title=request.POST["song"])
                articles.song = song
            articles.user = request.user
            articles.save()
            return redirect("main")
    else:
        articles_form = ArticlesForm()
    context = {
        "articles_form": articles_form,
    }
    return render(request, "articles/articles_create.html", context)


def song_search(request):
    search_data = request.GET.get("search", "")
    song = Song.objects.filter(song_title__icontains=search_data).all()
    song_list = []
    for s in song:
        song_list.append(
            {
                "name": s.song_title,
                "url": s.song_url,
                "thumbnail": s.song_thumbnail,
                "id": s.pk,
            }
        )
    context = {
        "song_list": song_list,
    }
    return JsonResponse(context)


def articles_detail(request, articles_pk):
    articles = get_object_or_404(Articles, pk=articles_pk)
    if request.user.is_authenticated:
        happy = Sympathy.objects.filter(articles=articles, user=request.user, feeling=1)
        sad = Sympathy.objects.filter(articles=articles, user=request.user, feeling=2)
        angry = Sympathy.objects.filter(articles=articles, user=request.user, feeling=3)
        funny = Sympathy.objects.filter(articles=articles, user=request.user, feeling=4)
    else:
        happy = 0
        sad = 0
        angry = 0
        funny = 0
    
    context = {
        "articles": articles,
        "comment_form": CommentForm(),
        "comments": articles.comment_set.all(),
        "articles_declaration_form": ArticlesDeclarationForm(),
        "comment_declaration_form": CommentDeclarationForm(),
        'f1':happy,
        'f2':sad,
        'f3':angry,
        'f4':funny,
    }
    return render(request, "articles/articles_detail.html", context)


@login_required
def articles_delete(request, articles_pk):
    articles = get_object_or_404(Articles, pk=articles_pk)
    if request.user == articles.user:
        articles.delete()
        return redirect("articles:articles_index")  # ????????? ????????????????
    return redirect("articles:articles_detail", articles_pk)


@login_required
def articles_update(request, articles_pk):
    articles = get_object_or_404(Articles, pk=articles_pk)
    if request.user == articles.user:
        if request.method == "POST":
            articles_form = ArticlesForm(request.POST, request.FILES, instance=articles)
            if articles_form.is_valid():
                article = articles_form.save(commit=False)
                if request.POST["song"]:
                    so = Song.objects.get(song_title=request.POST["song"])
                    articles.song = so
                article.save()

            return redirect("articles:articles_detail", articles_pk)
        else:
            articles_form = ArticlesForm(instance=articles)
        context = {
            "articles_form": articles_form,
        }
        return render(request, "articles/articles_update.html", context)
    else:
        messages.warning(request, "???????????? ?????? ??? ??? ????????????.")
        return redirect("articles:articles_index")


@login_required
def comment_create(request, articles_pk):
    articles = get_object_or_404(Articles, pk=articles_pk)
    result = request.POST["parent"]

    if request.method == "POST":  # POST????????????
        if request.user.is_authenticated:  # ???????????? ?????????
            # ????????? ???
            if int(result) == 0:
                comment_form = CommentForm(request.POST)  # POST?????? ????????? ????????? ?????????
                if comment_form.is_valid():  # ????????? ????????????
                    comment = comment_form.save(commit=False)  # ?????? ??????
                    # ????????? ??????
                    comment.articles = articles
                    comment.user = request.user
                    # ??????
                    comment.save()

                    context = {
                        "articles_pk": articles_pk,
                        "comment_pk": comment.pk,
                        "content": comment.content,
                        "userName": comment.user.username,
                    }
                    return JsonResponse(context)

            elif int(result) > 0:
                comment_form = CommentForm(request.POST)  # POST?????? ????????? ????????? ?????????
                if comment_form.is_valid():  # ????????? ????????????
                    comment = comment_form.save(commit=False)  # ?????? ??????
                    # ????????? ??????
                    comment.articles = articles
                    comment.user = request.user
                    comment.parent_id = result
                    # ??????
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

# ?????? ??????
# ??????
@login_required
def happy(request, articles_pk):
    articles = Articles.objects.get(pk=articles_pk)
    sympathy = Sympathy.objects.filter(articles=articles, user=request.user, feeling=1)
    if sympathy:
        sympathy.delete()
        s = False
    else:
        Sympathy.objects.create(articles=articles, user=request.user, feeling=1)
        s = True
    data = {
        's': s,
    }
    return JsonResponse(data)
# ??????
def sad(request, articles_pk):
    articles = Articles.objects.get(pk=articles_pk)
    sympathy = Sympathy.objects.filter(articles=articles, user=request.user, feeling=2)
    if sympathy:
        sympathy.delete()
        s = False
    else:
        Sympathy.objects.create(articles=articles, user=request.user, feeling=2)
        s = True
    data = {
        's': s,
    }
    return JsonResponse(data)
# ??????
def angry(request, articles_pk):
    articles = Articles.objects.get(pk=articles_pk)
    sympathy = Sympathy.objects.filter(articles=articles, user=request.user, feeling=3)
    if sympathy:
        sympathy.delete()
        s = False
    else:
        Sympathy.objects.create(articles=articles, user=request.user, feeling=3)
        s = True
    data = {
        's': s,
    }
    return JsonResponse(data)
# ??????
def funny(request, articles_pk):
    articles = Articles.objects.get(pk=articles_pk)
    sympathy = Sympathy.objects.filter(articles=articles, user=request.user, feeling=4)
    if sympathy:
        sympathy.delete()
        s = False
    else:
        Sympathy.objects.create(articles=articles, user=request.user, feeling=4)
        s = True
    data = {
        's': s,
    }
    return JsonResponse(data)


# ????????? ??????
from django.db import IntegrityError


@login_required
def articles_declaration(request, articles_pk):
    articles = Articles.objects.get(pk=articles_pk)
    if request.method == "POST":
        articles_declaration_form = ArticlesDeclarationForm(request.POST)
        if articles_declaration_form.is_valid():
            try:
                declaration = articles_declaration_form.save(commit=False)
                declaration.reporter = request.user
                declaration.reported = articles.user
                declaration.articles = articles
                articles_declaration_form.save()
                messages.warning(request, "?????????????????????.")
                return redirect("articles:articles_detail", articles_pk)
            except IntegrityError:
                messages.info(request, '?????? ????????? ??????????????????.')
                return redirect("articles:articles_detail", articles_pk)
    else:
        articles_declaration_form = ArticlesDeclarationForm()
    context = {
        "articles_declaration_form": articles_declaration_form,
    }
    return render(request, "articles/articles_detail.html", context)


@login_required
def comment_declaration(request, articles_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == "POST":
        comment_declaration_form = CommentDeclarationForm(request.POST)
        if comment_declaration_form.is_valid():
            try:
                declaration = comment_declaration_form.save(commit=False)
                declaration.reporter = request.user
                declaration.reported = comment.user
                declaration.comment = comment
                comment_declaration_form.save()
                messages.warning(request, "?????????????????????.")
                return redirect("articles:articles_detail", articles_pk)
            except IntegrityError:
                messages.info(request, '?????? ????????? ???????????????.')
                return redirect("articles:articles_detail", articles_pk)
    else:
        comment_declaration_form = ArticlesDeclarationForm()
    context = {
        "comment_declaration_form": comment_declaration_form,
    }
    return render(request, "articles/articles_detail.html", context)


def id_sort(request):
    jsonObject = json.loads(request.body)
    target_id = jsonObject.get("target_id")

    temp_results_user = Articles.objects.all().filter(user=request.user)
    temp_results = temp_results_user.filter(Q(created_at__contains=target_id))

    if temp_results:
        results = 1
    else:
        results = 0

    context = {
        "results": results,
    }

    return JsonResponse({"results": results})


def calendar_detail(request, date):
    temp_results_user = Articles.objects.all().filter(user=request.user)
    temp_results = temp_results_user.filter(Q(created_at__contains=date)).order_by('-created_at')
    dates = date.split('-')
    year = dates[0]
    month = dates[1]
    date = dates[2]
    context = {
        "diaries": temp_results,
        "year": year,
        "month": month,
        "date": date
    }
    return render(request, "articles/calendar_detail.html", context)
