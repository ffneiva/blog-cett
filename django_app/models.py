from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Blog(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    url = models.SlugField(max_length=100, unique=True)
    corpo = models.TextField()
    data = models.DateField(db_index=True, auto_now_add=True)
    categoria = models.ForeignKey('django_app.Categoria', on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='blog/', default='logo.png')

    def __unicode__(self):
        return '%s' % self.titulo
    
    def get_url_absoluta(self):
        return reverse('ver_post', kwargs={ 'slug': self.url })
    
    def get_comentarios(self):
        return sorted(Comentario.objects.filter(blog=self), lambda x: x.data)

class Categoria(models.Model):
    titulo = models.CharField(max_length=100, db_index=True)
    url = models.SlugField(max_length=100, db_index=True)

    def __unicode__(self):
        return '%s' % self.titulo
    
    def get_url_absoluta(self):
        return reverse('inicio', kwargs={ 'categoria_selecionada': self.titulo })

class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    texto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    editado = models.DateTimeField(null=True, blank=True)

class Resposta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE, related_name='respostas')
    texto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    editado = models.DateTimeField(null=True, blank=True)
