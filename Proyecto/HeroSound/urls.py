from django.urls import path
from HeroSound import views
from .views import start_music, cargar_music, busqueda


urlpatterns = [
    path('/', views.start_music),
    path('base_canciones/', views.base, name='basecancion'),
    path('cargar_music/', views.cargar_music, name='cargar_music'),
    path('busqueda/', views.busqueda, name='busqueda'),  
]