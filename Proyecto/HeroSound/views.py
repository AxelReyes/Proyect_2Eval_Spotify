from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from HeroSound.models import Cancion, Perfil, Playlist
from .forms import FormularioCancion, RegistroForm, CustomAuthenticationForm
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.core.serializers import serialize
import json

def start_music(request):
    # Obtén todas las canciones guardadas
    canciones = Cancion.objects.all().order_by('titulo')  # Ordena las canciones por el título

    # Verifica si se está realizando una búsqueda
    if 'q' in request.GET:
        query = request.GET.get('q')
        canciones = Cancion.objects.filter(titulo__icontains=query)
        resultados = [{'titulo': cancion.titulo, 'artista': cancion.artista} for cancion in canciones]
        return JsonResponse(resultados, safe=False)

    # Si no hay búsqueda, renderiza la plantilla con todas las canciones
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
            return redirect('administrador')  # Use the URL pattern name
    else:
        formulario = FormularioCancion()
    return render(request, 'HeroSound/upload_music.html', {'formulario': formulario})

@login_required
def base(request):
    canciones = Cancion.objects.all().order_by('titulo')  # Ordena las canciones por el título
    return render(request, 'HeroSound/base_canciones.html', {'canciones': canciones})

def detalle_cancion(request):
    canciones = Cancion.objects.all().order_by('titulo')  # Ordena las canciones por el título

    # Si hay parámetros GET, usa esos valores, de lo contrario usa la primera canción en la lista
    nombre_cancion = request.GET.get('nombreCancion', canciones.first().titulo if canciones.exists() else '')
    artista = request.GET.get('artista', canciones.first().artista if canciones.exists() else '')
    imagen_url = request.GET.get('imagenUrl', canciones.first().imagen.url if canciones.exists() else '')
    audio_url = request.GET.get('audioUrl', canciones.first().archivo_mp3.url if canciones.exists() else '')

    context = {
        'nombre_cancion': nombre_cancion,
        'artista': artista,
        'imagen_url': imagen_url,
        'url': audio_url,
        'canciones': canciones,
    }
    return render(request, 'HeroSound/detalle_cancion.html', context)

def show_administrador(request):
    canciones = Cancion.objects.all().order_by('titulo')  # Ordena las canciones por el título

    return render(request, 'HeroSound/administrador.html', {'canciones': canciones})


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            tipo_usuario = form.cleaned_data.get('tipo_usuario')
            
            # Crear un nuevo usuario
            user = User.objects.create_user(username=username, password=password)
            
            # Crear un perfil asociado al usuario
            Perfil.objects.create(user=user, tipo_usuario=tipo_usuario)
                
            # Iniciar sesión con el nuevo usuario
            login(request, user)
            return redirect('/')
    else:
        # Si el usuario no está autenticado, inicializar el formulario sin ningún tipo de usuario
        if not request.user.is_authenticated:
            form = RegistroForm()
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
                    return redirect('administrador')  # Use the URL pattern name
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

@login_required
def agregar_a_playlist(request):
    if request.method == 'POST':
        # Obtener los datos JSON de la solicitud
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': str(e)}, status=400)

        # Obtener el usuario actual
        usuario = request.user

        # Obtener o crear la playlist del usuario
        playlist, creado = Playlist.objects.get_or_create(user=usuario)

        # Obtener la información de la canción
        url = data.get('url')
        nombre_cancion = data.get('nombreCancion')
        artista = data.get('artista')
        imagen_url = data.get('imagenUrl')

        # Buscar si la canción ya existe en la base de datos
        cancion_existente = Cancion.objects.filter(titulo=nombre_cancion, artista=artista).first()

        if cancion_existente:
            # La canción ya existe, simplemente agrégala a la playlist
            playlist.canciones.add(cancion_existente)
        else:
            # La canción no existe, crea una nueva instancia de Cancion y agrégala a la playlist
            nueva_cancion = Cancion.objects.create(
                titulo=nombre_cancion,
                artista=artista,
                archivo_mp3=url,
                imagen=imagen_url
            )
            playlist.canciones.add(nueva_cancion)

        # Retorna una respuesta JSON indicando que la canción fue agregada exitosamente a la playlist
        return JsonResponse({'mensaje': 'Canción agregada exitosamente a la playlist'})

    # Si la solicitud no es de tipo POST, retornar un error
    return JsonResponse({'error': 'Se esperaba una solicitud de tipo POST'}, status=405)

@login_required
def ver_playlist(request):
    # Obtén la playlist del usuario actual
    playlist_usuario = Playlist.objects.filter(user=request.user).first()

    # Si el usuario no tiene una playlist, crea una vacía
    if not playlist_usuario:
        playlist_usuario = Playlist.objects.create(user=request.user)

    # Obtén las canciones de la playlist del usuario
    canciones_playlist = playlist_usuario.canciones.all()

    # Renderiza la plantilla con las canciones en el contexto
    return render(request, 'HeroSound/ver_playlist.html', {'canciones_playlist': canciones_playlist})

@login_required
def eliminar_cancion_playlist(request):
    if request.method == 'POST':
        # Obtener el ID de la canción a eliminar
        cancion_id = request.POST.get('cancion_id')
        
        # Obtener la playlist del usuario actual
        playlist_usuario = Playlist.objects.get(user=request.user)
        
        # Eliminar la canción de la playlist
        playlist_usuario.canciones.remove(cancion_id)
        
        # Redirigir de vuelta a la página de la lista de reproducción
        return redirect('ver_playlist')
    # Si la solicitud no es de tipo POST, redirigir a alguna página de error
    return redirect('ver_playlist')  # Podrías redirigir a una página de error 405, por ejemplo