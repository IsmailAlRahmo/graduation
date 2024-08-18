import React, { useState, useEffect, useRef } from "react";
import { LineChart } from "@mui/x-charts";
import io from "socket.io-client";

const Performance = ({ recording }) => {
  const socketRef = useRef(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [seconds, setSeconds] = useState([]);
  //   const [data, setData] = useState([]);
  const [latestMessage, setLatestMessage] = useState("");

  useEffect(() => {
    if (socketRef.current) {
      socketRef.current.on("server_message", (message) => {
        console.log(message.message);
        setLatestMessage(message.message);
      });
    }
  }, [recording]);
  useEffect(() => {
    if (recording) {
      console.log("recording started");

      // Connect to the Socket.IO server
      socketRef.current = io("http://127.0.0.1:5001");

      socketRef.current.on("server_message", (message) => {
        console.log(message.message); // Print the message to the console
      });

      // Access the user's camera
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
          videoRef.current.srcObject = stream;
          // Capture a frame every second
          const captureInterval = setInterval(() => {
            captureFrame();
          }, 1000);
          // Clean up on component unmount or when recording stops
          return () => {
            clearInterval(captureInterval);
            socketRef.current.disconnect();
          };
        })
        .catch((error) => console.error("Error accessing camera: ", error));
    } else {
      // Stop the video stream if recording is false
      if (videoRef.current && videoRef.current.srcObject) {
        let tracks = videoRef.current.srcObject.getTracks();
        tracks.forEach((track) => track.stop());
        videoRef.current.srcObject = null;
        socketRef.current.emit("stop_video");
      }
    }
  }, [recording]);

  const captureFrame = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");

    // Draw the video frame to the canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the canvas content to a base64-encoded image
    const frameData = canvas.toDataURL("image/jpeg");

    // Send the frame data to the server
    socketRef.current.emit("frame", frameData);

    // You can also update your state for the chart here if needed
    setSeconds((prev) => [...prev, prev.length + 1]);
    // setData((prev) => [...prev, Math.random() * 100]); // example data
  };

  return (
    <div className="w-3/6">
      <div className="w-full h-4/6 bg-[#192533] opacity-85 rounded-2xl flex flex-col">
        <h1 className="text-slate-200 font-thin text-center pt-4">
          Your performance chart{" "}
        </h1>
        {/* <div className="w-full h-full px-4 py-4">
          <LineChart
            className="w-full h-full"
            grid={{ horizontal: true }}
            xAxis={[{ scaleType: "point", data: seconds }]}
            series={[{ type: "line", data: data }]}
            sx={{
              "& .MuiChartsAxis-left .MuiChartsAxis-line": {
                stroke: "#94a3b8",
              },
              "& .MuiChartsAxis-left .MuiChartsAxis-tick": {
                stroke: "#94a3b8",
              },
              "& .MuiChartsAxis-left": {
                stroke: "#94a3b8",
              },
              "& .MuiChartsAxis-bottom .MuiChartsAxis-line ": {
                stroke: "#94a3b8",
              },
              "& .MuiChartsAxis-bottom .MuiChartsAxis-tick": {
                stroke: "#94a3b8",
              },
              "& .MuiChartsAxis-bottom": {
                stroke: "#94a3b8",
              },
              "& .MuiChartsGrid-line": {
                stroke: "#94a3b8",
              },
            }}
          />
        </div> */}
      </div>
      <div className="text-white text-center pt-8 text-2xl h-2/6 ease-in-out">
        Time spent: {seconds.length > 1 ? seconds.length - 1 : "0"} seconds
      </div>
      <div className="message">{latestMessage}</div>
      {/* Hidden video and canvas elements */}
      <video ref={videoRef} style={{ display: "none" }} autoPlay />
      <canvas
        ref={canvasRef}
        width="640"
        height="480"
        // style={{ display: "none" }}
      />
    </div>
  );
};

export default Performance;
