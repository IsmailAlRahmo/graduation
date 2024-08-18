import io from "socket.io-client";
import { Link } from "react-router-dom";
import { useEffect, useMemo, useRef, useState } from "react";

// import { PATHS } from "../../paths";

import "./VideoOverlay.css";

const VideoOverlayComponent = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const socketRef = useRef(null);
  const messagesEndRef = useRef(null);
  const captureIntervalRef = useRef(null);
  const recordTimeIntervalRef = useRef(null);

  const [messages, setMessages] = useState([]);
  const [chartImg, setChartImg] = useState(null);
  const [recording, setRecording] = useState(false);
  const [recordTime, setRecordTime] = useState(0);

  const messagesToDisplay = useMemo(() => {
    const temp = [];
    messages.forEach((msg) => {
      if (temp[temp.length - 1] !== msg) {
        temp.push(msg);
      }
    });
    return temp;
  });

  useEffect(() => {
    console.log("fire");
    socketRef.current = io("http://localhost:5001");

    socketRef.current.on("server_message", (message) => {
      console.log(message.message); // Print the message to the console
      setMessages((prevMessages) => [...prevMessages, message.message]);
    });

    socketRef.current.on("plan", (chartImg) => {
      setChartImg(chartImg);
    });

    navigator.mediaDevices
      .getUserMedia({ video: true, audio: true })
      .then((stream) => {
        videoRef.current.srcObject = stream;
        videoRef.current.onloadedmetadata = () => {
          videoRef.current
            .play()
            .catch((error) => console.error("Error playing video:", error));
        };
      })
      .catch((error) => console.error("Error accessing webcam:", error));

    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
    };
  }, []);

  useEffect(() => {
    // Scroll to the bottom of the messages when new messages arrive
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  function captureFrame() {
    
    const canvas = canvasRef.current;
    const video = videoRef.current;
    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL("image/jpeg");
    socketRef.current.emit("frame", dataURL);
    console.log("frame sent",dataURL);
  }

  function handleToggleRecording() {
    if (recording) {
      setRecording(false);
      setRecordTime(0);
      clearInterval(recordTimeIntervalRef.current);
      clearInterval(captureIntervalRef.current); // Clear the interval to stop capturing frames
      socketRef.current.emit("stop_video"); // Inform the server that video feed is stopped
      console.log("stop video");
    } else {
      console.log("start video");
      setRecording(true);
      recordTimeIntervalRef.current = setInterval(() => {
        setRecordTime((pre) => pre + 1);
      }, 1000);
      captureIntervalRef.current = setInterval(captureFrame, 500);
    }
  }

  function convertSecondsToMinSecString(_seconds) {
    let minutes = Math.floor(_seconds / 60).toString();
    if (minutes.length === 1) {
      minutes = `0${minutes}`;
    }
    let seconds = (_seconds - minutes * 60).toString();
    if (seconds.length === 1) {
      seconds = `0${seconds}`;
    }

    return `${minutes}:${seconds}`;
  }

  return (
    <div className="overlay">
      <div className="content-container">
        <div className="messages-section">
          <h3>Messages</h3>
          <ul>
            {messagesToDisplay.map((msg, index) => (
              <li key={index}>{msg}</li>
            ))}
            <div ref={messagesEndRef} />
          </ul>
        </div>
        <div className="plan-section">
          <h3>Plan</h3>
          {chartImg ? (
            <img
              src={chartImg}
              alt="Plan"
              style={{
                maxWidth: "100%",
                maxHeight: "100%",
                borderRadius: "5px",
              }}
            />
          ) : (
            <p>No plan data available</p>
          )}
        </div>
        <div className="camera-section">
          <video ref={videoRef} className="video-element" />
          {recording && (
            <div className="flex gap-2 items-center absolute top-10 right-3">
              <span className="text-red-900 text-2xl mb-1 duration-1000 animate-ping">
                ●
              </span>
              {recordTime !== 0 ? (
                <span className="">
                  {convertSecondsToMinSecString(recordTime)}
                </span>
              ) : null}
            </div>
          )}
          <canvas
            ref={canvasRef}
            width="640"
            height="480"
            style={{ display: "none" }}
          />
        </div>
      </div>
      <div className="button-container">
        <button
          onClick={handleToggleRecording}
          className="toggle-recording-btn"
        >
          {recording ? "End Recording" : "Start Recording"}
        </button>
      </div>
      <span className="absolute top-3 right-3">
        {/* <Link
          to={PATHS.dashboard}
          className="bg-red-500 text-white px-2 py-1 hover:bg-red-400 hover:text-gray-300 rounded-lg"
        >
          close
        </Link> */}
      </span>
    </div>
  );
};

export default VideoOverlayComponent;
