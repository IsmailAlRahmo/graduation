import React, { useState, useEffect, useRef } from "react";
import io from "socket.io-client";

const Advice = ({ recording }) => {
  const [feedback, setFeedback] = useState([]);
  const socketRef = useRef(null);

  useEffect(() => {
    // Connect to the Socket.IO server
    socketRef.current = io("http://127.0.0.1:5001", {
      transports: ["polling"],
    });

    socketRef.current.on("connect", () => {
      console.log("Connected to the audio server");
    });

    socketRef.current.on("server_message", (data) => {
      console.log("Server message:", data);
    });

    socketRef.current.on("audio_message", (data) => {
      console.log("Audio message:", data);
      // Add new message to feedback array
      setFeedback((prevFeedback) => [...prevFeedback, data.message]);
      // Emit start_recording event
      if (recording) {
        socketRef.current.emit("start_recording");
      }
    });

    socketRef.current.on("audio_status", (data) => {
      console.log("Audio status:", data);
    });

    return () => {
      socketRef.current.disconnect();
    };
  }, [recording]);

  useEffect(() => {
    if (recording) {
      // Emit the start_recording event when recording starts
      socketRef.current.emit("start_recording");
    }
  }, [recording]);

  return (
    <div className="w-5/12 h-full bg-[#192533] opacity-85 rounded-2xl overflow-y-scroll no-scrollbar">
      <div className="pt-4">
        <h1 className="text-slate-200 font-thin text-center">Advice & Notes</h1>
        <ul className="text-slate-300 font-light text-center">
          {feedback.map((message, index) => (
            <li key={index}>{message}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Advice;
