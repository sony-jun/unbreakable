from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [

    path("", views.articles_index, name="articles_index"),
    path("articles_create/", views.articles_create, name="articles_create"),
    path(
        "<int:articles_pk>/articles_detail/",
        views.articles_detail,
        name="articles_detail",
    ),
    path(
        "<int:articles_pk>/articles_delete/",
        views.articles_delete,
        name="articles_delete",
    ),
    path(
        "<int:articles_pk>/articles_update/",
        views.articles_update,
        name="articles_update",
    ),
]