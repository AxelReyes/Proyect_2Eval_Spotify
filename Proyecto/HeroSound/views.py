from django.shortcuts import render, redirect
from HeroSound.models import Cancion   # Importa tu modelo Cancion
from . import forms
from .forms import FormularioCancion

# Create your views here.
def index(request):
    cancionlist2 = Cancion.objects.order_by('titulo')
    my_context = {'cancion': cancionlist2}
    return render(request, 'HeroSound/index.html', context=my_context)


def start_music(request):
    # Obtén todas las canciones guardadas
    canciones = Cancion.objects.all()
    
    return render(request, 'HeroSound/lista_canciones.html', {'canciones': canciones})


def cargar_music(request):
    if request.method == 'POST':
        formulario = FormularioCancion(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('/HeroSound/canciones/')
    else:
        formulario = FormularioCancion()
    return render(request, 'HeroSound/upload_music.html', {'formulario': formulario})

def base(request):
    canciones = Cancion.objects.all()
    return render(request, 'HeroSound/base_canciones.html',{'canciones': canciones})