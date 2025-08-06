from django.contrib import admin
from .models import Alumnos
from .models import Comentario
from .models import ComentarioContacto

# Register your models here.
class AdministrarModelo(admin.ModelAdmin):
    readonly_fields = ('created','updated')
    list_display =('matricula','nombre','carrera','turno','created')
    search_fields=('matricula','nombre','carrera','turno')
    date_hierarchy='created'
    list_filter=('carrera','turno')

    list_per_page=2
    list_display_links=('matricula', 'nombre')
    list_editable=('turno',)

    def get_readonly_fields(self, request, obj = None):
        if request.user.groups.filter(name="usuarios").exists():
            return('created', 'updated', 'matricula', 'carrera', 'turno')
        else:
            return('created','updated')

    
admin.site.register(Alumnos, AdministrarModelo)

class AdministarComentarios(admin.ModelAdmin):
    list_display = ('id', 'coment')
    search_fields = ('id', 'created')
    date_hierarchy = 'created'
    readonly_fields = ('created', 'id')

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name="grupo1").exists():
            return ('created', 'alumno')
        else:
            return ('created',)

admin.site.register(Comentario, AdministarComentarios)

class AdministrarComentariosContacto(admin.ModelAdmin):
    list_display=('id','mensaje')
    search_fields = ('id','created')
    date_hierarchy= 'created'
    readonly_fields=('created','id')

admin.site.register(ComentarioContacto, AdministrarComentariosContacto)

