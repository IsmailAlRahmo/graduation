import React, { useEffect, useRef, useState } from "react";
import io from "socket.io-client";

const socket = io("http://localhost:5000"); // Connect to Flask server

function DummyWebSocket() {
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  // useEffect for listening to server messages
  // useEffect(() => {
  //   socket.on("server_message", (data) => {
  //     console.log("Server Message:", data);
  //   });

  //   // Cleanup on component unmount
  //   return () => {
  //     socket.off("server_message");
  //   };
  // }, []);
  // useEffect for capturing and sending audio chunks every 15 seconds
  useEffect(() => {
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then((stream) => {
        mediaRecorderRef.current = new MediaRecorder(stream);

        mediaRecorderRef.current.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunksRef.current.push(event.data);
          }
        };

        // Start and stop recording every 15 seconds
        const startRecording = () => {
          audioChunksRef.current = [];
          mediaRecorderRef.current.start();
          setTimeout(() => {
            mediaRecorderRef.current.stop();
          }, 30000);
        };

        // When recording stops, send the accumulated audio chunks
        mediaRecorderRef.current.onstop = () => {
          const audioBlob = new Blob(audioChunksRef.current, {
            type: "audio/webm",
          });

          // Ensure the Blob size is even
          const blobSize = audioBlob.size;
          const evenSize = blobSize % 2 === 0 ? blobSize : blobSize - 1;

          // Slice the Blob to make sure the size is even
          const evenBlob = audioBlob.slice(0, evenSize);
          socket.emit("audio", evenBlob);
          socket.on("server_message", (data) => {
            console.log("Server Message:", data);
          });
          startRecording(); // Start recording again after sending data
        };

        startRecording(); // Initial start of recording
      })
      .catch((error) => console.error("Error accessing media devices:", error));

    // Cleanup on component unmount
    return () => {
      if (
        mediaRecorderRef.current &&
        mediaRecorderRef.current.state !== "inactive"
      ) {
        mediaRecorderRef.current.stop();
      }
    };
  }, []);

  return (
    <div>
      <h1>React & Flask Socket.IO Example</h1>
    </div>
  );
}

export default DummyWebSocket;
