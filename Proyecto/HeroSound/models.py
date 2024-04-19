from django.db import models

# Create your models here.
class Cancion(models.Model):
    titulo = models.CharField(max_length=100)
    artista = models.CharField(max_length=100)
    archivo_mp3 = models.FileField(upload_to='canciones/')
    imagen = models.ImageField(upload_to='imagenes/', blank=True, null=True)
    
    #Representar el registro como cadena de texto
    def __str__(self):
        return self.titulo