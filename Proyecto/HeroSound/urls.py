from django.urls import path
from HeroSound import views
from .views import start_music, cargar_music, busqueda, detalle_cancion


urlpatterns = [
    path('/', views.start_music),
    path('base_canciones/', views.base, name='basecancion'),
    path('cargar_music/', views.cargar_music, name='cargar_music'),
    path('busqueda/', views.busqueda, name='busqueda'),  
    path('detalle_cancion/', views.detalle_cancion, name='detalle_cancion'),
]