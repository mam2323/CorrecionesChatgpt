// Ocultar y mostrar el header al hacer scroll
let lastScrollTop = 0; // Variable para guardar la última posición del scroll
const header = document.querySelector('header'); // Seleccionamos el header

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset || document.documentElement.scrollTop;

    header.style.transform = (currentScroll > lastScrollTop && currentScroll > header.offsetHeight)
        ? 'translateY(-100%)'
        : 'translateY(0)';

    lastScrollTop = Math.max(0, currentScroll);
});

// Mostrar/Ocultar el formulario de edición del perfil
const editarPerfilBtn = document.getElementById('editar-perfil-btn');
const datosPerfil = document.getElementById('datos-perfil');
const formularioEditarPerfil = document.getElementById('formulario-editar-perfil');

if (editarPerfilBtn && datosPerfil && formularioEditarPerfil) {
    editarPerfilBtn.addEventListener('click', () => {
        const isHidden = formularioEditarPerfil.style.display === 'none' || formularioEditarPerfil.style.display === '';

        formularioEditarPerfil.style.display = isHidden ? 'block' : 'none';
        datosPerfil.style.display = isHidden ? 'none' : 'block';
        editarPerfilBtn.textContent = isHidden ? 'Cancelar' : 'Editar Perfil';
    });
}

// Previsualización y eliminación de imágenes al cargar en publicar_producto
document.addEventListener('DOMContentLoaded', () => {
    const inputImagenes = document.getElementById('imageness');
    const previewContainer = document.getElementById('preview-container');
    let filesToUpload = []; // Array para almacenar las imágenes seleccionadas

    if (inputImagenes && previewContainer) {
        inputImagenes.addEventListener('change', (event) => {
            const newFiles = Array.from(event.target.files);

            if (filesToUpload.length + newFiles.length > 8) {
                alert('Solo puedes subir un máximo de 8 imágenes.');
                return;
            }

            newFiles.forEach(file => {
                if (!filesToUpload.some(f => f.name === file.name && f.size === file.size)) {
                    filesToUpload.push(file);
                }
            });

            updatePreview();
        });

        function updatePreview() {
            previewContainer.innerHTML = '';

            filesToUpload.forEach((file, index) => {
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        const previewItem = document.createElement('div');
                        previewItem.classList.add('preview-item');

                        const img = document.createElement('img');
                        img.src = e.target.result;
                        img.alt = 'Previsualización';

                        if (index === 0) {
                            const mainImageLabel = document.createElement('span');
                            mainImageLabel.textContent = 'Imagen Principal';
                            mainImageLabel.classList.add('main-image-label');
                            previewItem.appendChild(mainImageLabel);
                        }

                        const deleteButton = document.createElement('button');
                        deleteButton.textContent = '×';
                        deleteButton.classList.add('delete-button');

                        deleteButton.addEventListener('click', () => {
                            filesToUpload.splice(index, 1);
                            updatePreview();
                        });

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

// Manejar favoritos en productos
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.btn-favorito').forEach(boton => {
        boton.addEventListener('click', function () {
            const productoId = this.dataset.productoId;
            const isFavorite = this.dataset.isFavorite === 'true';
            const url = isFavorite
                ? `/favoritos/eliminar/${productoId}/`
                : `/favoritos/agregar/${productoId}/`;

            fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (['added', 'removed'].includes(data.status)) {
                        const icon = this.querySelector('i');
                        this.dataset.isFavorite = data.status === 'added';
                        icon.classList.toggle('fas', data.status === 'added');
                        icon.classList.toggle('far', data.status === 'removed');
                        icon.style.color = data.status === 'added' ? 'red' : 'gray';
                    }
                })
                .catch(console.error);
        });
    });
});
