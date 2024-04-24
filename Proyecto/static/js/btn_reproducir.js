var reproductor = document.getElementById('reproductor');

function reproducir(url, nombreCancion, artista, imagenUrl) {
    // Detener la canción actual si está reproduciendo
    reproductor.pause();
    reproductor.currentTime = 0;

    // Cargar y reproducir la nueva canción
    reproductor.src = url;
    reproductor.play();

    // Mostrar información de la canción en el footer
    var nombreArtistaCancionDiv = document.getElementById('nombre-artista-cancion');
    var imagenDiv = document.getElementById('imagen'); // Definir imagenDiv

    nombreArtistaCancionDiv.innerHTML = `${artista}  <br>${nombreCancion}`;

    // Crear elemento img para mostrar la imagen
    var imagenElement = document.createElement('img');
    imagenElement.src = imagenUrl;
    imagenElement.alt = 'Carátula de la canción';
    imagenElement.width = 100; // ajusta el ancho según sea necesario
    // Añadir la imagen al div de la imagen
    imagenDiv.innerHTML = '';
    imagenDiv.appendChild(imagenElement);
}