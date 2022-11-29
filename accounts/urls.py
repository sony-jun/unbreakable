from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # CRUD
    path('', views.index, name="index"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('<int:user_pk>/update/', views.update, name="update"),
    path('<int:user_pk>/delete/', views.delete, name="delete"),
    path('<int:user_pk>/profile/', views.profile, name="profile"),
    path('password/', views.password, name="password"),
    
    # 카카오 소셜 로그인
    path('kakao/login/callback/', views.kakao_callback, name="kakao_callback"),
    path('kakao/login/', views.kakao_request, name="kakao"),
    # 메시지(쪽지)
    path('<int:user_pk>/<int:articles_pk>/message_create/', views.message_create, name="message_create"),
]
