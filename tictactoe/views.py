from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages    
from django.contrib.messages import constants

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
        dono = User(id = request.session['id_user'])

        privada = request.POST.get('privada')
        
        if privada:
            senha = request.POST.get('senha')
            room = Room(dono = dono,
                        privada = True,
                        senha = senha,
                        )
            
        else: room = Room(dono = dono)
            
        room.save()
                
        return redirect('room', room.code)


@login_required(login_url='login')
def entrar(request):
    if request.method == 'GET':
        rooms = Room.objects.filter(vencedor=None)
        return render(request, 'entrar.html', {'rooms': rooms})
    
    elif request.method == 'POST':
        senha = request.POST.get('senha')
        room_id = request.POST.get('room_id')
        
        room = Room.objects.get(id = room_id)
                
        if senha == room.senha:
            return redirect('room', room.code)
        
        messages.add_message(request, constants.ERROR, 'Senha da sala incorreta.')
        return redirect('entrar')
        


@login_required(login_url='login')
def jogo(request, code):
    
    return render(request, 'jogo.html', {'code': code})
