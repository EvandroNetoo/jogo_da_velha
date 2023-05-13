from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('criar/', views.criar, name='criar'),
    path('entrar/', views.entrar, name='entrar'),
    path('<str:code>/', views.jogo, name='room')
]
