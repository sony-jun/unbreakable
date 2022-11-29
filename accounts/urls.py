from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('<int:user_pk>/update/', views.update, name="update"),
    path('<int:user_pk>/profile/', views.profile, name="profile"),
    path('<int:user_pk>/delete/', views.delete, name="delete"),
    path('password/', views.password, name="password"),
    path('kakao/login/callback/', views.kakao_callback, name="kakao_callback"),
    path('kakao/login/', views.kakao_request, name="kakao"),
]
