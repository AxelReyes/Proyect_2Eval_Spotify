from django.contrib.auth.models import User
from django.db import models

class Cancion(models.Model):
    titulo = models.CharField(max_length=100)
    artista = models.CharField(max_length=100)
    archivo_mp3 = models.FileField(upload_to='canciones/')
    imagen = models.ImageField(upload_to='imagenes/', blank=True, null=True)
    
    def __str__(self):
        return self.titulo

class Perfil(models.Model):
    USUARIO_CHOICES = (
        ('administrador', 'Administrador'),
        ('user', 'User'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=20, choices=USUARIO_CHOICES)
    
    def __str__(self):
        return f'{self.user.username} - {self.get_tipo_usuario_display()}'