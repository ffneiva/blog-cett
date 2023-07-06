from django import template
from django_app.models import Categoria

register = template.Library()

@register.filter
def filtrar_categorias(posts):
    categorias = Categoria.objects.filter(blog__in=posts).distinct()
    return categorias
