function reproducir(url, nombreCancion, artista, imagenUrl) {
    
    var audio = document.getElementById('reproductor');
    var playPauseButton = document.getElementById('play-pause');
    var imagenDiv = document.getElementById('imagen');
    var nombreArtistaCancionDiv = document.getElementById('nombre-artista-cancion');

    // Detener la canción actual si está reproduciendo
    audio.pause();
    audio.currentTime = 0;

    // Cargar y reproducir la nueva canción
    audio.src = url;
    audio.play();

    // Mostrar información de la canción en el footer
    nombreArtistaCancionDiv.innerHTML = `${artista} <br>${nombreCancion}`;

    // Crear elemento img para mostrar la imagen
    var imagenElement = document.createElement('img');
    imagenElement.src = imagenUrl;
    imagenElement.alt = 'Carátula de la canción';

    // Crear el botón de detalle
    var detailButton = document.createElement('a');
    detailButton.innerHTML = `
        <img class="flecha" src="https://cdn-icons-png.flaticon.com/512/5344/5344570.png" alt="expandir" style="position: absolute; top: 4.8rem; left: 5rem; width: 2rem;">
    `;
    detailButton.onclick = function() {
        mostrarDetalle(nombreCancion, artista, imagenUrl, url);
    };

    // Añadir la imagen y el botón al div de la imagen
    imagenDiv.innerHTML = '';
    imagenDiv.appendChild(detailButton);
    // imagenDiv.appendChild(detailButton);
    imagenDiv.appendChild(imagenElement);

    // // Crear botón de detalle
    // var detailButton = document.createElement('button');
    // detailButton.className = 'button_detail';
    // detailButton.style.backgroundColor = '#0f6db9af'; 
    // detailButton.style.width = '1rem';
    // detailButton.style.height = '1rem';
    // detailButton.style.borderTopRightRadius = '1rem';
    // detailButton.style.position = 'fixed';
    // detailButton.style.marginLeft = '5.5rem';
    // detailButton.onclick = function() {
    //     mostrarDetalle(nombreCancion, artista, imagenUrl, url);
    // };

    // Cambia el estado del botón a "pause"
    playPauseButton.classList.add('pause');

    // Actualiza el botón de play/pause para que pause el audio si se hace clic
    playPauseButton.removeEventListener('click', togglePlayPause);
    playPauseButton.addEventListener('click', togglePlayPause);
}

// Función para manejar el cambio de play a pause y viceversa
function togglePlayPause() {
    var audio = document.getElementById('reproductor');
    var playPauseButton = document.getElementById('play-pause');

    if (audio.paused) {
        audio.play();
        playPauseButton.classList.add('pause');
    } else {
        audio.pause();
        playPauseButton.classList.remove('pause');
    }
}

// Función para redirigir al usuario a la página de detalle_cancion.html
function mostrarDetalle(nombreCancion, artista, imagenUrl, url) {
    // Construir la URL para el detalle de la canción con todos los parámetros
    var detalleUrl = `/HeroSound/detalle_cancion/?nombreCancion=${encodeURIComponent(nombreCancion)}&artista=${encodeURIComponent(artista)}&imagenUrl=${encodeURIComponent(imagenUrl)}&audioUrl=${encodeURIComponent(url)}`;
    // Redireccionar al usuario a la página de detalle_cancion.html
    window.location.href = detalleUrl;

}

// Función para expandir y contraer la imagen con animación
function toggleExpandCollapse() {
    var imagenDiv = document.getElementById('imagen');
    var toggleButton = document.getElementById('toggle-button');

    if (imagenDiv.classList.contains('expanded')) {
        imagenDiv.style.height = '0';
        toggleButton.innerText = 'Expandir';
        imagenDiv.classList.remove('expanded');
    } else {
        imagenDiv.style.height = '200px'; // Cambia el valor de altura según tu necesidad
        toggleButton.innerText = 'Contraer';
        imagenDiv.classList.add('expanded');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var audio = document.getElementById('reproductor');
    var playPauseButton = document.getElementById('play-pause');
    var seekBar = document.getElementById('seek-bar');
    var currentTimeDisplay = document.getElementById('current-time');
    var durationTimeDisplay = document.getElementById('duration-time');
    var volumenBar = document.getElementById('volumen-bar');

    function formatTime(seconds) {
        var minutes = Math.floor(seconds / 60);
        var seconds = Math.floor(seconds % 60);
        if (seconds < 10) {
            seconds = '0' + seconds;
        }
        return minutes + ':' + seconds;
    }

    // Play/Pause button functionality
    playPauseButton.addEventListener('click', togglePlayPause);

    // Seek bar functionality
    seekBar.addEventListener('input', function() {
        var seekTime = audio.duration * (seekBar.value / 100);
        audio.currentTime = seekTime;
    });

    // Update the seek bar and time display as the audio plays
    audio.addEventListener('timeupdate', function() {
        var value = (audio.currentTime / audio.duration) * 100;
        seekBar.value = value;

        // Update the custom property to change the seek bar color
        seekBar.style.setProperty('--seek-bar-value', value + '%');

        currentTimeDisplay.textContent = formatTime(audio.currentTime);
        durationTimeDisplay.textContent = formatTime(audio.duration);
    });

    // Update duration time once metadata is loaded
    audio.addEventListener('loadedmetadata', function() {
        durationTimeDisplay.textContent = formatTime(audio.duration);
    });

    // Volume control functionality
    volumenBar.addEventListener('input', function() {
        audio.volume = volumenBar.value;
    });
});