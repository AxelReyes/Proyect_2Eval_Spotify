resultadoBusqueda.style.display = "none";

inputBusqueda.addEventListener('input', function () {
    const query = inputBusqueda.value.trim();
    if (query.length > 0) {
        fetch(`/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                mostrarResultados(data);
                // Mostrar el contenedor de resultados después de obtener los datos
                resultadoBusqueda.style.display = "block";
            });
    } else {
        // Si la búsqueda está vacía, ocultar el contenedor de resultados
        resultadoBusqueda.innerHTML = '';
        resultadoBusqueda.style.display = "none";
    }
});


function mostrarResultados(data) {
    resultadoBusqueda.innerHTML = '';
    const query = inputBusqueda.dataset.query; // Obtener el valor de query del elemento input
    if (data.length === 0) {
        resultadoBusqueda.innerHTML = '<p>No se encontraron resultados</p>';
    } else {
        data.forEach(cancion => {
            const elementoCancion = document.createElement('div');
            const enlaceCancion = document.createElement('a');
            enlaceCancion.textContent = `${cancion.titulo} - ${cancion.artista}`;
            // Adjuntar el valor de query al enlace como un atributo de datos
            enlaceCancion.dataset.query = query;
            enlaceCancion.addEventListener('click', function() {
                // Obtener el valor de query del enlace al que se hizo clic
                const clickedQuery = this.dataset.query;
                window.location.href = `/HeroSound/busqueda/?q=${cancion.titulo}`;
            });
            elementoCancion.appendChild(enlaceCancion);
            resultadoBusqueda.appendChild(elementoCancion);
        });
    }
}
