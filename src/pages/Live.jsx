import { FaPlayCircle } from "react-icons/fa";
import Advice from "../components/Advice";
import Performance from "../components/Performance";
import { FaPause } from "react-icons/fa";
import { useEffect, useRef, useState } from "react";
import { io } from "socket.io-client";
import { useUser } from "../auth/useUser";
import { useNavigate } from "react-router-dom";

const Live = () => {
  const { user } = useUser();
  const [recording, setRecording] = useState(false); // Use boolean instead of 0/1
  const [feedback, setFeedback] = useState([]);
  const [redirect, setRedirect] = useState(false);
  const [chartpoints, setChartpoints] = useState([]);
  const socketRef = useRef(null);
  const navigate = useNavigate();

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
    });
    socketRef.current.on("performance_update", (data) => {
      console.log("performance_update message:", data);
      // setChartpoints((prevFeedback) => [...prevFeedback, data.message]);
    });
    socketRef.current.on("video_message", (data) => {
      setFeedback((prevFeedback) => {
        // Check if the new message is the same as the last one added
        if (
          prevFeedback.length > 0 &&
          prevFeedback[prevFeedback.length - 1] === data.message
        ) {
          // If it's the same, return the previous feedback unchanged
          return prevFeedback;
        }

        // Otherwise, add the new message to the feedback array
        return [...prevFeedback, data.message];
      });
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
      const userId = user.id;
      socketRef.current.emit("start_recording");
      socketRef.current.emit("start_video_recording", userId);
      console.log("Start command sent to the server");
    }
    if (!recording) {
      socketRef.current.emit("stop_recording");
      console.log("Stop command sent to the server");
      // Redirect after 5 seconds
    }
    if (redirect) {
      setTimeout(() => {
        navigate("/home/reports");
      }, 10000);
    }
  }, [recording]);
  useEffect(() => {
    const handlePerformanceUpdate = (data) => {
      console.log("performance_update message:", data);
      const time = Math.floor(data.time); // Get integer value of time
      const score = data.score;

      setChartpoints((prevPoints) => [
        ...prevPoints,
        { time, score }, // Add new data point to chartpoints
      ]);
    };

    // Assuming socketRef.current is initialized and valid
    socketRef.current.on("performance_update", handlePerformanceUpdate);

    // Clean up the socket listener when the component unmounts
  }, []);
  const handleRecordingToggle = () => {
    if (recording) {
      setRecording((prevRecording) => !prevRecording);
      setRedirect((prevRedirect) => !prevRedirect);
    } else {
      setRecording((prevRecording) => !prevRecording);
    }
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
