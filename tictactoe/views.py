from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect

from autenticacao.decorators import login_required
from .models import Room
from autenticacao.models import User


@login_required(login_url='login')
def home(request):
    
    return render(request,'home.html')


@login_required(login_url='login')
def criar(request):
    if request.method == 'GET':
        return render(request,'criar.html')
    if request.method == 'POST':

        room = Room()
        room.save()
                
        return redirect('room', room.code)


@login_required(login_url='login')
def entrar(request):
    rooms = Room.objects.filter(vencedor=None)
    return render(request, 'entrar.html', {'rooms': rooms})


@login_required(login_url='login')
def jogo(request, code):
    
    return render(request, 'jogo.html', {'code': code})
