from django.shortcuts import render, redirect, get_object_or_404
from django_app.models import Blog, Categoria, Comentario, Resposta
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
import json


def logar(request):
    context = {
        'categorias': Categoria.objects.all(),
    }
    return render(request, 'registration/login.html', context)

def cadastrar(request):
    context = {
        'categorias': Categoria.objects.all(),
    }
    return render(request, 'django/cadastrar.html', context)

def inicio(request, categoria_selecionada='Todas'):
    categorias = Categoria.objects.all()
    if request.GET.get('categoria') == 'Todas':
        posts = Blog.objects.all().order_by('-data')[:10]
    elif request.GET.get('categoria'):
        categoria_filtrada = Categoria.objects.filter(titulo=request.GET.get('categoria'))
        categoria_selecionada = categoria_filtrada[0].titulo
        posts = Blog.objects.filter(categoria__in=categoria_filtrada).order_by('-data')[:10]
    else:
        posts = Blog.objects.all().order_by('-data')[:10]

    context = {
        'categorias': categorias,
        'posts': posts,
        'categoria_selecionada': categoria_selecionada,
    }
    return render(request, 'django/inicio.html', context)

def sobre(request):
    with open('static/json/sobre.json', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)

    context = {
        'categorias': Categoria.objects.all(),
        'dados': dados,
    }
    return render(request, 'django/sobre.html', context)

def ver_post(request, slug):
    blog = get_object_or_404(Blog, url=slug)
    context = {
        'categorias': Categoria.objects.all(),
        'post': blog,
        'comentarios': Comentario.objects.filter(blog_id=blog.id)
            .prefetch_related('respostas__usuario')
            .select_related('usuario')
            .order_by('data', 'respostas__data'),
    }
    return render(request, 'django/post.html', context)

def perfil(request):
    usuario = User.objects.filter(username=request.user.username)
    context = {
        'categorias': Categoria.objects.all(),
        'usuario': usuario,
        # 'comentarios': usuario.get_comentarios(),
    }
    return render(request, 'django/perfil.html', context)

def fazer_cadastro(request):
    if request.method == 'POST':
        usuario = User.objects.filter(email=request.POST.get('email')).first()
        if not usuario:
            usuario = User(
                username=request.POST.get('username'),
                email=request.POST.get('email'),
                password=make_password(request.POST.get('senha')),
            )
            usuario.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return logar(request)
        else:
            messages.error(request, 'Usuário já possui conta.')
            return logar(request)
    
def fazer_login(request):
    if request.method == 'POST':
        usuario = User.objects.filter(email=request.POST.get('email')).first()
        if usuario:
            if check_password(request.POST.get('senha'), usuario.senha):
                user = authenticate(request, email=usuario.email, senha=request.POST.get('senha'))
                if user is not None:
                    login(request, user)
                    return render(request, 'django/inicio.html')
                else:
                    messages.error(request, 'Falha na autenticação.')
            else:
                messages.error(request, 'Senha incorreta.')
        else:
            messages.error(request, 'Usuário não possui conta.')
    return render(request, 'django/login.html')

def adicionar_comentario(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        comentario = request.POST.get('comentario')
        if comentario:
            novo_comentario = Comentario(
                usuario=request.user,
                blog=blog,
                texto=comentario,
            )
            novo_comentario.save()
            messages.success(request, 'Comentário adicionado com sucesso!')
        else:
            messages.error(request, 'Erro ao adicionar comentário.')
    return redirect(reverse('ver_post', args=[blog.url]))

def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    blog = get_object_or_404(Blog, id=comentario.blog_id)
    if request.method == 'POST':
        if comentario:
            comentario.texto = request.POST.get('comentario')
            comentario.editado = datetime.now()
            comentario.save()
            messages.success(request, 'Comentário atualizado com sucesso!')
        else:
            messages.error(request, 'Erro ao atualizar comentário.')
    return redirect(reverse('ver_post', args=[blog.url]))

def responder_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    blog = get_object_or_404(Blog, id=comentario.blog_id)
    if request.method == 'POST':
        if comentario:
            resposta = Resposta(
                usuario=request.user,
                comentario=comentario,
                texto=request.POST.get('comentario'),
            )
            resposta.save()
            messages.success(request, 'Resposta adicionada com sucesso!')
        else:
            messages.error(request, 'Erro ao adicionar resposta.')
    return redirect(reverse('ver_post', args=[blog.url]))


def editar_resposta(request, resposta_id):
    resposta = get_object_or_404(Resposta, id=resposta_id)
    comentario = get_object_or_404(Comentario, id=resposta.comentario_id)
    blog = get_object_or_404(Blog, id=comentario.blog_id)
    if request.method == 'POST':
        if resposta:
            resposta.texto = request.POST.get('resposta')
            resposta.editado = datetime.now()
            resposta.save()
            messages.success(request, 'Resposta atualizada com sucesso!')
        else:
            messages.error(request, 'Erro ao atualizar resposta.')
    return redirect(reverse('ver_post', args=[blog.url]))

def atualizar_perfil(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('nome')
        request.user.last_name = request.POST.get('sobrenome')
        request.user.save()
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil')
    messages.error(request, 'Erro ao atualizar perfil.')
    return render(request, 'django/perfil.html')
