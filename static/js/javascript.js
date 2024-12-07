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
