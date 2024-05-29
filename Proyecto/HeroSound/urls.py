from django.urls import path
from HeroSound import views
from .views import start_music, cargar_music, busqueda, detalle_cancion, login_view
from .views import logout_view, registro, show_administrador, eliminar_cancion


urlpatterns = [
    path('/', views.start_music),
    path('base_canciones/', views.base, name='basecancion'),
    path('cargar_music/', views.cargar_music, name='cargar_music'),
    path('busqueda/', views.busqueda, name='busqueda'),  
    path('detalle_cancion/', views.detalle_cancion, name='detalle_cancion'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('administrador/', views.show_administrador, name='administrador'),  
    path('editar_cancion/<int:cancion_id>/', views.editar_cancion, name='editar_cancion'),
    path('eliminar_cancion/<int:cancion_id>/', views.eliminar_cancion, name='eliminar_cancion'),

  
]