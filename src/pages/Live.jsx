import { FaPlayCircle } from "react-icons/fa";
import Advice from "../components/Advice";
import Performance from "../components/Performance";
import { FaPause } from "react-icons/fa";
import { useEffect, useRef, useState } from "react";
import { io } from "socket.io-client";

const Live = () => {
  const [recording, setRecording] = useState(false); // Use boolean instead of 0/1
  const [feedback, setFeedback] = useState([]);
  const [chartpoints, setChartpoints] = useState([]);
  const socketRef = useRef(null);

  useEffect(() => {
    // Establish a socket connection
    socketRef.current = io("http://127.0.0.1:5001", {
      transports: ["websocket"], // Try using "websocket" instead of "polling"
    });

    socketRef.current.on("connect", () => {
      console.log("Connected to the audio server");
    });

    socketRef.current.on("server_message", (data) => {
      console.log("Server message:", data);
    });

    socketRef.current.on("audio_message", (data) => {
      console.log("Audio message:", data);
      setFeedback((prevFeedback) => [...prevFeedback, data.message]);
      // socketRef.current.emit("start_recording");
      // console.log("Start command sent to the server");
    });

    socketRef.current.on("audio_status", (data) => {
      console.log("Audio status:", data);
    });

    return () => {
      socketRef.current.disconnect();
      console.log("Disconnected from the audio server");
    };
  }, []);

  useEffect(() => {
    if (recording) {
      const userId = 1;
      socketRef.current.emit("start_recording");
      socketRef.current.emit("start_video_recording", userId);
      console.log("Start command sent to the server");
    } else {
      socketRef.current.emit("stop_recording");
      console.log("Stop command sent to the server");
    }
  }, [recording]);

  const handleRecordingToggle = () => {
    setRecording((prevRecording) => !prevRecording);
  };

  return (
    <div className="w-full h-screen bg-black px-24 py-20">
      <div className="w-full h-full flex justify-evenly">
        <Advice feedback={feedback} />
        <Performance chartpoints={chartpoints} />
      </div>
      <div className="text-center flex justify-center">
        <button onClick={handleRecordingToggle}>
          {recording ? (
            <FaPause className="w-12 h-12 text-[#DD310B]" />
          ) : (
            <FaPlayCircle className="w-12 h-12 text-slate-400" />
          )}
        </button>
      </div>
    </div>
  );
};

export default Live;
