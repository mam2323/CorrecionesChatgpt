import React from 'react';
import ChatRoom from './ChatRoom'; // Asegúrate de que la ruta es correcta

function App() {
    return (
        <div>
            <h1>Bienvenido al Chat</h1>
            <ChatRoom roomName="mi-sala" /> {/* Agrega el componente ChatRoom */}
        </div>
    );
}

export default App;
