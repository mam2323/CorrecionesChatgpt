// Mostrar lista de conversaciones
function showChatList() {
  document.getElementById('chat-list').classList.remove('hidden');
  document.getElementById('chat-room').classList.add('hidden');
}

// Mostrar chat activo
function showChatRoom() {
  document.getElementById('chat-list').classList.add('hidden');
  document.getElementById('chat-room').classList.remove('hidden');
}

// Detectar si es un dispositivo móvil
function isMobile() {
  return window.innerWidth <= 768;
}

// Detectar clicks en las conversaciones
document.querySelectorAll('.conversation').forEach(item => {
  item.addEventListener('click', function (e) {
      if (isMobile()) { // Solo para móviles
          e.preventDefault();
          const roomId = this.getAttribute('data-room-id'); // Obtén el room_id del elemento
          window.location.href = `?room_id=${roomId}`; // Cambia la URL para incluir el room_id
          showChatRoom(); // Muestra el chat
      }
  });
});

// Manejar el botón "Atrás" en móviles
document.getElementById('back-button').addEventListener('click', function () {
  if (isMobile()) {
      window.location.href = "?"; // Redirige a la lista de conversaciones
      showChatList();
  }
});

// Manejar la carga inicial para móviles
window.addEventListener('load', function () {
  const params = new URLSearchParams(window.location.search);
  const roomId = params.get('room_id');

  if (isMobile()) {
      if (roomId) {
          showChatRoom(); // Si hay un room_id, muestra el chat
      } else {
          showChatList(); // Si no hay room_id, muestra la lista
      }
  }
});
