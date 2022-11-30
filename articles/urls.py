from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("calendar", views.calendar, name="calendar"),
    path("calendar_1", views.calendar_1, name="calendar_1"),
    path("", views.articles_index, name="articles_index"),
    path("articles_create/", views.articles_create, name="articles_create"),
    path("<int:articles_pk>/articles_detail/", views.articles_detail, name="articles_detail"),
    path("<int:articles_pk>/articles_delete/", views.articles_delete, name="articles_delete"),
    path("<int:articles_pk>/articles_update/", views.articles_update, name="articles_update"),
    path("<int:articles_pk>/articles_detail/comments/", views.comment_create, name="comment_create"),
    path("<int:articles_pk>/articles_detail/comments/<int:comment_pk>/comment_delete/", views.comment_delete, name="comment_delete"),
]
