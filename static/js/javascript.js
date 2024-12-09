let lastScrollTop = 0; // Variable para guardar la última posición del scroll
const header = document.querySelector('header'); // Seleccionamos el header

// Detectamos cuando se hace scroll en la página
window.addEventListener('scroll', function() {
    let currentScroll = window.pageYOffset || document.documentElement.scrollTop; // Posición actual del scroll

    // Si estamos bajando la página y ya hemos desplazado el header fuera de vista, lo ocultamos
    if (currentScroll > lastScrollTop && currentScroll > header.offsetHeight) {
        header.style.transform = 'translateY(-100%)'; // Ocultamos el header moviéndolo hacia arriba
    } else {
        // Si estamos subiendo la página, mostramos el header de nuevo
        header.style.transform = 'translateY(0)'; // Lo ponemos en su posición original
    }

    // Actualizamos la última posición del scroll
    lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
});




// Mostrar/Ocultar el formulario de edición y los datos del perfil
const editarPerfilBtn = document.getElementById('editar-perfil-btn'); // Botón de editar
const datosPerfil = document.getElementById('datos-perfil'); // Div con datos del perfil
const formularioEditarPerfil = document.getElementById('formulario-editar-perfil'); // Formulario de edición

if (editarPerfilBtn && datosPerfil && formularioEditarPerfil) {
    editarPerfilBtn.addEventListener('click', function () {
        // Alternar visibilidad de los datos del perfil y el formulario
        if (formularioEditarPerfil.style.display === 'none' || formularioEditarPerfil.style.display === '') {
            formularioEditarPerfil.style.display = 'block'; // Mostrar formulario
            datosPerfil.style.display = 'none'; // Ocultar datos del perfil
            editarPerfilBtn.textContent = 'Cancelar'; // Cambiar texto del botón
        } else {
            formularioEditarPerfil.style.display = 'none'; // Ocultar formulario
            datosPerfil.style.display = 'block'; // Mostrar datos del perfil
            editarPerfilBtn.textContent = 'Editar Perfil'; // Restaurar texto del botón
        }
    });
}


//Previsualizacion de la imagen de perfil
document.addEventListener("DOMContentLoaded", function () {
    const inputImagenes = document.getElementById("imagenes");
    const previewContainer = document.getElementById("preview-container");

    if (inputImagenes) {
        inputImagenes.addEventListener("change", function (event) {
            previewContainer.innerHTML = ""; // Limpiar las previsualizaciones previas

            Array.from(event.target.files).forEach(file => {
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    reader.onload = function (e) {
                        const img = document.createElement('img');
                        img.src = e.target.result;
                        img.alt = "Previsualización";
                        img.style.width = "100px";
                        img.style.borderRadius = "5px";
                        img.style.marginRight = "10px";
                        previewContainer.appendChild(img);
                    };
                    reader.readAsDataURL(file);
                }
            });
        });
    }
});
