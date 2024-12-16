import React, { useState, useEffect } from 'react';

function ChatRoom({ roomName }) {
    const [socket, setSocket] = useState(null);
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        const chatSocket = new WebSocket(`ws://django:8000/ws/chat/${roomName}/`);

        chatSocket.onopen = () => {
            console.log("Conectado al WebSocket");
        };

        chatSocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setMessages((prevMessages) => [...prevMessages, data.message]);
        };

        chatSocket.onclose = (event) => {
            console.error("WebSocket cerrado:", event);
        };

        chatSocket.onerror = (error) => {
            console.error("Error en WebSocket:", error);
        };

        setSocket(chatSocket);

        return () => {
            chatSocket.close();
        };
    }, [roomName]);

    const sendMessage = () => {
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({ message: "Hola, desde React!" }));
        }
    };

    return (
        <div>
            <h1>Chat Room: {roomName}</h1>
            <div>
                {messages.map((msg, index) => (
                    <p key={index}>{msg}</p>
                ))}
            </div>
            <button onClick={sendMessage}>Enviar Mensaje</button>
        </div>
    );
}

export default ChatRoom;
