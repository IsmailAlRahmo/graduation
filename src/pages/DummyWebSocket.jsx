// src/DummyWebSocket.js

import React, { useEffect } from 'react';
import { w3cwebsocket as W3CWebSocket } from 'websocket';

// const client = new W3CWebSocket('ws://localhost:8000/ws/images/');

const DummyWebSocket = () => {
  // useEffect(() => {
  //   // Function to send a dummy message
  //   const sendMessage = () => {
  //     const message = "This is a dummy message";
  //     client.send(JSON.stringify({ message }));
  //   };

  //   // Send a message every 5 seconds
  //   const intervalId = setInterval(() => {
  //     sendMessage();
  //   }, 5000);

  //   // Handle messages from the server
  //   client.onmessage = (message) => {
  //     const dataFromServer = JSON.parse(message.data);
  //     console.log('Received message from server:', dataFromServer.message);
  //   };

  //   // Clean up interval on component unmount
  //   return () => clearInterval(intervalId);
  // }, []);

  return (
    <div>
      <h1>WebSocket Test</h1>
    </div>
  );
};

export default DummyWebSocket;
