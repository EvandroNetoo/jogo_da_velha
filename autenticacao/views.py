from django.shortcuts import render, redirect
from django.contrib import messages    
from django.contrib.messages import constants

from .decorators import only_unauth, login_required
from .models import User


@only_unauth(home_url = 'home')
def cadastro(request):
    if request.method == 'GET':        
        return render(request, 'cadastro.html')
    
    elif request.method == 'POST':
        usuario = request.POST.get('usuario').strip().lower()
        senha = request.POST.get('senha').strip()
        
        user = User(usuario=usuario,
                    senha=senha,
                    )
        user.save()
        
        messages.add_message(request, constants.SUCCESS, 'Cadastrado com sucesso.')
        
        return redirect('login')


@only_unauth(home_url = 'home')
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    elif request.method == 'POST':
        usuario = request.POST.get('usuario').strip().lower()
        senha = request.POST.get('senha').strip()
        
        user = User.objects.filter(usuario=usuario,
                                   senha=senha,
                                   ).first()
        
        if not user:
            messages.add_message(request, constants.ERROR, 'Usuário e/ou senha inválidos.')
            return redirect('login')
        
        request.session['id_user'] = user.id
        return redirect('home')
    

@login_required(login_url = 'home')
def sair(request):
    request.session['id_user'] = None
    messages.add_message(request, constants.SUCCESS, 'Deslogado com sucesso.')
    return redirect('login')
