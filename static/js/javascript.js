// Ocultar y mostrar el header al hacer scroll
let lastScrollTop = 0; // Variable para guardar la última posición del scroll
const header = document.querySelector('header'); // Seleccionamos el header

window.addEventListener('scroll', function () {
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

// Mostrar/Ocultar el formulario de edición del perfil
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

// Previsualización y eliminación de imágenes al cargar en publicar_producto
document.addEventListener("DOMContentLoaded", function () {
    const inputImagenes = document.getElementById("imageness");
    const previewContainer = document.getElementById("preview-container");
    let filesToUpload = []; // Array para almacenar las imágenes seleccionadas

    if (inputImagenes && previewContainer) {
        // Manejar el evento de cambio en el input de imágenes
        inputImagenes.addEventListener("change", function (event) {
            const newFiles = Array.from(event.target.files);

            // Verificar el total de imágenes seleccionadas
            if (filesToUpload.length + newFiles.length > 8) {
                alert("Solo puedes subir un máximo de 8 imágenes.");
                return;
            }

            // Agregar nuevas imágenes al array sin reemplazar las existentes
            newFiles.forEach((file) => {
                if (!filesToUpload.some(f => f.name === file.name && f.size === file.size)) {
                    filesToUpload.push(file);
                }
            });

            updatePreview(); // Actualizar la previsualización
        });

        // Función para actualizar la previsualización de las imágenes
        function updatePreview() {
            previewContainer.innerHTML = ""; // Limpiar previsualización previa

            filesToUpload.forEach((file, index) => {
                if (file.type.startsWith("image/")) {
                    const reader = new FileReader();
                    reader.onload = function (e) {
                        // Crear contenedor para imagen y eliminar botón
                        const previewItem = document.createElement("div");
                        previewItem.style.position = "relative";
                        previewItem.style.display = "inline-block";
                        previewItem.style.margin = "10px";

                        const img = document.createElement("img");
                        img.src = e.target.result;
                        img.alt = "Previsualización";
                        img.style.width = "100px";
                        img.style.height = "100px";
                        img.style.objectFit = "cover";
                        img.style.borderRadius = "5px";

                        // Añadir texto "Imagen principal" a la primera imagen
                        if (index === 0) {
                            const mainImageLabel = document.createElement("span");
                            mainImageLabel.textContent = "Imagen Principal";
                            mainImageLabel.style.position = "absolute";
                            mainImageLabel.style.top = "5px";
                            mainImageLabel.style.left = "5px";
                            mainImageLabel.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
                            mainImageLabel.style.color = "white";
                            mainImageLabel.style.padding = "2px 5px";
                            mainImageLabel.style.borderRadius = "3px";
                            mainImageLabel.style.fontSize = "10px";
                            previewItem.appendChild(mainImageLabel);
                        }

                        const deleteButton = document.createElement("button");
                        deleteButton.textContent = "×";
                        deleteButton.style.position = "absolute";
                        deleteButton.style.top = "0";
                        deleteButton.style.right = "0";
                        deleteButton.style.backgroundColor = "red";
                        deleteButton.style.color = "white";
                        deleteButton.style.border = "none";
                        deleteButton.style.borderRadius = "50%";
                        deleteButton.style.cursor = "pointer";
                        deleteButton.style.width = "20px";
                        deleteButton.style.height = "20px";

                        // Manejar eliminación de la imagen
                        deleteButton.addEventListener("click", function () {
                            filesToUpload.splice(index, 1); // Eliminar del array
                            updatePreview(); // Actualizar la previsualización
                        });

                        // Añadir imagen y botón al contenedor
                        previewItem.appendChild(img);
                        previewItem.appendChild(deleteButton);
                        previewContainer.appendChild(previewItem);
                    };
                    reader.readAsDataURL(file);
                }
            });
        }
    }
});
