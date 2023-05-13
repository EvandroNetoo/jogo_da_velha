from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('home')),
    path('admin/', admin.site.urls),
    path('auth/', include('autenticacao.urls')),
    path('jogo/', include('tictactoe.urls')),
]
