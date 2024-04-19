from django.urls import path
from HeroSound import views
from .views import start_music, cargar_music


urlpatterns = [
    path('', views.index),
    path('canciones/', start_music, name='canciones'),
    path('cargar_music/', cargar_music, name='cargar_music'),
]