from django.shortcuts import render, redirect
from HeroSound.models import Cancion   # Importa tu modelo Cancion
from . import forms
from .forms import FormularioCancion
from django.http import JsonResponse

# Create your views here.
# def index(request):
#     cancionlist2 = Cancion.objects.order_by('titulo')
#     my_context = {'cancion': cancionlist2}
#     return render(request, 'HeroSound/index.html', context=my_context)


def start_music(request):
    # Obtén todas las canciones guardadas
    canciones = Cancion.objects.all()
    
    # Verifica si se está realizando una búsqueda
    if 'q' in request.GET:
        query = request.GET.get('q')
        canciones = Cancion.objects.filter(titulo__icontains=query)
        resultados = [{'titulo': cancion.titulo, 'artista': cancion.artista} for cancion in canciones]
        return JsonResponse(resultados, safe=False)
    
    # Si no hay búsqueda, renderiza la plantilla con todas las canciones
    return render(request, 'HeroSound/index.html', {'canciones': canciones})

def busqueda(request):
    cancion_seleccionada = None  # Inicializa la variable en caso de que no se encuentre la canción
    if 'q' in request.GET:
        query = request.GET.get('q')
        print("Query:", query)  # Verifica el valor de query en la consola
        try:
            # Busca una canción cuyo título coincida exactamente con query
            cancion_seleccionada = Cancion.objects.get(titulo__iexact=query)
        except Cancion.DoesNotExist:
            pass

    print("cancion_seleccionada: ", cancion_seleccionada)
    return render(request, 'HeroSound/resultados_busqueda.html', {'cancion_seleccionada': cancion_seleccionada})


def cargar_music(request):
    if request.method == 'POST':
        formulario = FormularioCancion(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('/')
    else:
        formulario = FormularioCancion()
    return render(request, 'HeroSound/upload_music.html', {'formulario': formulario})

def base(request):
    canciones = Cancion.objects.all()
    return render(request, 'HeroSound/base_canciones.html',{'canciones': canciones})