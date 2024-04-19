from django.shortcuts import render, redirect
from HeroSound.models import Cancion   # Importa tu modelo Cancion
from . import forms
from .forms import FormularioCancion

# Create your views here.
def index(request):
    cancionlist2 = Cancion.objects.order_by('titulo')
    my_context = {'cancion': cancionlist2}
    return render(request, 'HeroSound/index.html', context=my_context)
    #return HttpResponse("<h1>Recuerdo el día en que de la chamba yo me enamoré</h1>")

#Crear un formulario para mostrar
# def form_user_view(request):
#     form = forms.FormUser()

#     #print(request.method)
#     if request.method == 'POST':
#         form = forms.FormUser(request.POST)
#         if form.is_valid():
#             print("VALIDADO!")
#             print("Name: ", form.cleaned_data['name'])
#             print("Email: ", form.cleaned_data['email'])
#             print("Text: ", form.cleaned_data['text'])
#             print(form.cleaned_data['botcatcher'])
#             comment = Comments.objects.get_or_create(name=form.cleaned_data['name'],
#                                                      email=form.cleaned_data['email'], 
#                                                      text=form.cleaned_data['text'])[0]
#             comment.save()


#     return render(request, 'mi_primera_app/form_page.html', {'form' : form})


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