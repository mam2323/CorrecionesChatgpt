import React, { useState, useEffect } from 'react';

function ChatRoom({ roomName }) {
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
    const [socket, setSocket] = useState(null);

    useEffect(() => {
        const connectWebSocket = () => {
            const chatSocket = new WebSocket(`ws://localhost:8000/ws/chat/${roomName}/`);
    
            chatSocket.onopen = () => {
                console.log("WebSocket conectado");
            };
    
            chatSocket.onmessage = function (e) {
                const data = JSON.parse(e.data);
                setMessages((prevMessages) => [...prevMessages, data.message]);
            };
    
            chatSocket.onclose = function () {
                console.error("WebSocket desconectado. Intentando reconectar...");
                setTimeout(() => {
                    connectWebSocket();
                }, 1000);
            };
    
            chatSocket.onerror = function (error) {
                console.error("Error en WebSocket:", error);
            };
    
            setSocket(chatSocket);
        };
    
        connectWebSocket();
    }, [roomName]);
    
    // Función para enviar mensajes
    const sendMessage = () => {
        if (socket && socket.readyState === WebSocket.OPEN && newMessage.trim()) {
            socket.send(JSON.stringify({
                message: newMessage,
            }));
            setNewMessage('');
        } else {
            console.error("WebSocket no está listo para enviar mensajes.");
        }
    };

    return (
        <div>
            <div style={{ border: '1px solid #ccc', padding: '10px', height: '300px', overflowY: 'scroll' }}>
                {messages.map((msg, index) => (
                    <div key={index}>{msg}</div>
                ))}
            </div>
            <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                placeholder="Escribe un mensaje..."
            />
            <button
                onClick={sendMessage}
                disabled={!socket || socket.readyState !== WebSocket.OPEN} // Desactiva el botón si el socket no está listo
            >
                Enviar
            </button>
        </div>
    );
}

export default ChatRoom;
