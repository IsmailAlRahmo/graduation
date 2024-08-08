import React, { useRef, useCallback, useEffect } from "react";
import Webcam from "react-webcam";
import { w3cwebsocket as W3CWebSocket } from "websocket";

const client = new W3CWebSocket("ws://localhost:8000/ws/images/");

const StartRecording = () => {
//   const webcamRef = useRef(null);

  const capture = useCallback(() => {
    // if (webcamRef.current) {
    //   const imageSrc = webcamRef.current.getScreenshot({
    //     width: 320,
    //     height: 240,
    //   });
    //   if (imageSrc) {
    //     // Send the captured image to the backend via WebSocket
    //     client.send(JSON.stringify({ image: imageSrc }));
    //   }
    // }
    client.send(JSON.stringify({ image: imageSrc }));
  }, []);

  useEffect(() => {
    const intervalId = setInterval(() => {
      capture();
    }, 5000); // Capture image every 5 seconds

    client.onmessage = (message) => {
      const dataFromServer = JSON.parse(message.data);
      console.log(dataFromServer.message);
    };

    return () => clearInterval(intervalId);
  }, [capture]);

  return (
    <div>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={640}
        height={480}
      />
    </div>
  );
};

export default StartRecording;

// const StartRecording = () => {
//   return (
//     <div>StartRecording</div>
//   )
// }

// export default StartRecording
