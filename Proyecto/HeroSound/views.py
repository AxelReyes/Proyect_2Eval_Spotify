from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from HeroSound.models import Cancion, Perfil
from .forms import FormularioCancion, RegistroForm, CustomAuthenticationForm
from django.shortcuts import get_object_or_404
from django.urls import reverse

def start_music(request):
    canciones = Cancion.objects.all()
    if 'q' in request.GET:
        query = request.GET.get('q')
        canciones = Cancion.objects.filter(titulo__icontains(query))
        resultados = [{'titulo': cancion.titulo, 'artista': cancion.artista} for cancion in canciones]
        return JsonResponse(resultados, safe=False)
    return render(request, 'HeroSound/index.html', {'canciones': canciones})

def busqueda(request):
    cancion_seleccionada = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        try:
            cancion_seleccionada = Cancion.objects.get(titulo__iexact=query)
        except Cancion.DoesNotExist:
            pass
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

@login_required
def base(request):
    canciones = Cancion.objects.all()
    return render(request, 'HeroSound/base_canciones.html', {'canciones': canciones})

def detalle_cancion(request):
    canciones = Cancion.objects.all()
    nombre_cancion = request.GET.get('nombreCancion', '')
    artista = request.GET.get('artista', '')
    imagen_url = request.GET.get('imagenUrl', '')
    audio_url = request.GET.get('audioUrl', '')

    context = {
        'nombre_cancion': nombre_cancion,
        'artista': artista,
        'imagen_url': imagen_url,
        'url': audio_url,
        'canciones': canciones,
    }
    return render(request, 'HeroSound/detalle_cancion.html', context)

def show_administrador(request):
    canciones = Cancion.objects.all()
    if 'q' in request.GET:
        query = request.GET.get('q')
        canciones = Cancion.objects.filter(titulo__icontains(query))
        resultados = [{'titulo': cancion.titulo, 'artista': cancion.artista} for cancion in canciones]
        return JsonResponse(resultados, safe=False)
    return render(request, 'HeroSound/administrador.html', {'canciones': canciones})


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Establecer la contraseña
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Crear el perfil asociado al usuario registrado
            tipo_usuario = form.cleaned_data['tipo_usuario']
            perfil = Perfil.objects.create(user=user, tipo_usuario=tipo_usuario)
            
            # Iniciar sesión con el usuario registrado
            login(request, user)
            
            # Redirigir a la página principal o a donde desees
            return redirect('/')
    else:
        # Obtener el tipo de usuario actual del perfil
        perfil_usuario = get_object_or_404(Perfil, user=request.user)
        tipo_usuario_actual = perfil_usuario.tipo_usuario if perfil_usuario else 'user'
        
        # Inicializar el formulario con el tipo de usuario actual
        form = RegistroForm(initial={'tipo_usuario': tipo_usuario_actual})
    return render(request, 'registration/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Asegurarse de que el perfil exista
                perfil, created = Perfil.objects.get_or_create(user=user, defaults={'tipo_usuario': 'user'})
                if perfil.tipo_usuario == 'administrador':
                    return redirect('/HeroSound/administrador')
                elif perfil.tipo_usuario == 'user':
                    return redirect('/')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('/')

def editar_cancion(request, cancion_id):
    cancion = get_object_or_404(Cancion, id=cancion_id)

    if request.method == 'POST':
        formulario = FormularioCancion(request.POST, request.FILES, instance=cancion)
        if formulario.is_valid():
            formulario.save()
            return redirect(reverse('basecancion'))
    else:
        formulario = FormularioCancion(instance=cancion)

    return render(request, 'HeroSound/editar_cancion.html', {'formulario': formulario, 'cancion': cancion})

@login_required
def eliminar_cancion(request, cancion_id):
    cancion = get_object_or_404(Cancion, id=cancion_id)
    cancion.delete()
    return redirect('basecancion')