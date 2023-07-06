"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', view=views.inicio, name='inicio'),
    path('conta/', include('django.contrib.auth.urls')),
    path('admin/', view=admin.site.urls, name='admin'),
    path('logar/', view=views.logar, name='logar'),
    path('perfil/', view=views.perfil, name='perfil'),
    path('cadastrar/', view=views.cadastrar, name='cadastrar'),
    path('sobre/', view=views.sobre, name='sobre'),
    re_path(r'post/(?P<slug>[^\.]+).html', view=views.ver_post, name='ver_post'),
    path('fazer_cadastro', view=views.fazer_cadastro, name='fazer_cadastro'),
    path('fazer_login', view=views.fazer_login, name='fazer_login'),
    re_path(r'adicionar_comentario/(?P<blog_id>[^\.]+)', view=views.adicionar_comentario, name='adicionar_comentario'),
    re_path(r'editar_comentario/(?P<comentario_id>[^\.]+)', view=views.editar_comentario, name='editar_comentario'),
    re_path(r'responder_comentario/(?P<comentario_id>[^\.]+)', view=views.responder_comentario, name='responder_comentario'),
    re_path(r'editar_resposta/(?P<resposta_id>[^\.]+)', view=views.editar_resposta, name='editar_resposta'),
    path('atualizar_perfil/', view=views.atualizar_perfil, name='atualizar_perfil'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
