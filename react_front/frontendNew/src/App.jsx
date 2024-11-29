import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:5000'); // Update with your Flask server URL

const App = () => {
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        // Listen for 'mqtt_message' event
        socket.on('mqtt_message', (data) => {
            console.log('Message from MQTT:', data);
            setMessages((prev) => [...prev, data]);
        });

        // Cleanup on component unmount
        return () => socket.off('mqtt_message');
    }, []);

    return (
        <div>
            <h1>MQTT Messages</h1>
            <ul>
                {messages.map((msg, index) => (
                    <li key={index}>
                        Topic: {msg.topic}, Message: {msg.message}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default App;
