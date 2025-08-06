from django.shortcuts import render, redirect
from .models import Alumnos
from .forms import ComentarioContactoForm
from .models import ComentarioContacto
from django.shortcuts import get_object_or_404
import datetime
from .models import Archivos
from .forms import FormArchivos
from django.contrib import messages
# Create your views here.

def registros(request):
    alumnos =Alumnos.objects.all()
    return render(request, "registros/principal.html",{'alumnos':alumnos})

def comentarios(request):
    comentarios =ComentarioContacto.objects.all()
    return render(request,"registros/comentarios.html",{'comentarios':comentarios})

def registrar(request):
    if request.method =='POST':
        form = ComentarioContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("Comentarios")
    form =ComentarioContactoForm()
    return render(request,'registros/contacto.html', {'form': form})


def contacto(request):
    return render(request, "registros/contacto.html")

def eliminarComentarioContacto(request, id, confirmacion='registros/confirmarEliminacion.html'):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    
    if request.method == 'POST':
        comentario.delete()
        comentarios = ComentarioContacto.objects.all()
        return render(request, "registros/comentarios.html", {
            'comentarios': comentarios
        })
    
    return render(request, confirmacion, {
        'object': comentario
    })

def consultar1(request):
    alumnos=Alumnos.objects.filter(carrera="TI")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar2(request):
    alumnos=Alumnos.objects.filter(carrera="TI").filter(turno="matutino")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar3(request):
    alumnos = Alumnos.objects.all().only("matricula", "nombre", "carrera", "turno", "imagen")
    return render(request, "registros/consultas.html", {'alumnos': alumnos})

def consultar4(request):
    alumnos=Alumnos.objects.filter(turno__contains="Vesp")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar5(request):
    alumnos=Alumnos.objects.filter(nombre__in=["Juan","Ana"])
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar6(request):
    fechaInicio= datetime.date(2025, 6, 20)
    fechaFin=datetime.date(2025, 7, 25)
    alumnos=Alumnos.objects.filter(created__range=(fechaInicio,fechaFin))
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar7(request):
    alumnos=Alumnos.objects.filter(comentario__coment__contains="Se la pasa copiando codigo de IA")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar8(request):
    fechaInicio= datetime.date(2025, 7, 8)
    fechaFin=datetime.date(2025, 7, 9)
    comentarios =ComentarioContacto.objects.filter(created__range=(fechaInicio,fechaFin))
    return render(request,"registros/comentarios.html",{'comentarios': comentarios})

def consultar9(request):
    comentarios = ComentarioContacto.objects.filter(mensaje__icontains="Se la pasa copiando codigo de IA")
    return render(request, "registros/comentarios.html", {'comentarios': comentarios})

def consultar10(request):
    comentarios = ComentarioContacto.objects.filter(usuario__icontains="daniel")
    return render(request, "registros/consultas.html", {'comentarios': comentarios})

def consultar11(request):
    comentarios = ComentarioContacto.objects.only("mensaje")
    return render(request, "registros/consultas.html", {'comentarios': comentarios})

def consultar12(request):
    comentarios = ComentarioContacto.objects.filter(mensaje__startswith="Se")
    return render(request, "registros/comentarios.html", {'comentarios': comentarios})


def archivos(request):
    if request.method == 'POST':
        form = FormArchivos(request.POST, request.FILES)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            descripcion = form.cleaned_data['descripcion']
            archivo = form.cleaned_data['archivo']
            insert = Archivos(titulo=titulo, descripcion=descripcion, archivo=archivo)
            insert.save()
            messages.success(request, "Archivo guardado correctamente.")
            # Después de guardar, puedes limpiar el formulario para evitar resubmits:
            form = FormArchivos()
        else:
            messages.error(request, "Error al procesar el formulario.")
    else:
        form = FormArchivos()
    
    archivos_subidos = Archivos.objects.all().order_by('-created')
    return render(request, "registros/archivos.html", {
        'form': form,
        'archivos': archivos_subidos
    })


def consultasSQL(request):
    alumno = Alumnos.objects.raw(
        'SELECT id matricula, nombre, carrera, turno, imagen FROM registros_alumnos WHERE carrera="TI" ORDER BY turno DESC'
    )
    return render(request, "registros/consultas.html", {'alumno': alumno})


def seguridad(request, nombre=None):
    nombre = request.GET.get('nombre')
    return render(request,"registros/seguridad.html", {'nombre': nombre})



def consultarComentarioIndividual(request, id):
    comentario=ComentarioContacto.objects.get(id=id)
    return render(request, "registros/formEditarComentario.html",{'comentario':comentario})


def editarComentarioContacto(request, id):
    comentario= get_object_or_404(ComentarioContacto, id=id)
    form =ComentarioContactoForm(request.POST, instance= comentario)

    if form.is_valid():
        form.save()
        comentarios = ComentarioContacto.objects.all()
        return render(request, "registros/comentarios.html", {'comentarios':comentarios})
    
    return render(request, "registros/formEditarComentario.html", {'comentario':comentario})