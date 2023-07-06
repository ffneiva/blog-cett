from django.contrib import admin
from django_app.models import Blog, Categoria


class BlogAdmin(admin.ModelAdmin):
    exclude = ['data']
    list_display = ('titulo', 'url', 'categoria', 'corpo')
    list_filter = ('categoria',)
    search_fields = ['titulo', 'corpo']
    prepopulated_fields = {'url': ('titulo',)}
    
class CategoriaAdmin(admin.ModelAdmin):
    exclude = ['data']
    list_display = ('titulo', 'url')
    search_fields = ['titulo']
    prepopulated_fields = {'url': ('titulo',)}

admin.site.register(Blog, BlogAdmin)
admin.site.register(Categoria, CategoriaAdmin)
