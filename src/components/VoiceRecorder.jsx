import { useState } from "react";
import { ReactMic } from "react-mic";

const VoiceRecorder = () => {
  const [recording, setRecording] = useState(false);
  const [blobURL, setBlobURL] = useState(null);

  const startRecording = () => {
    setRecording(true);
  };

  const stopRecording = () => {
    setRecording(false);
  };

  const onStop = (recordedBlob) => {
    console.log(URL.createObjectURL(recordedBlob.blob));
    setBlobURL(URL.createObjectURL(recordedBlob.blob));
  };

  return (
    <div>
      <h1>Voice Recorder</h1>
      <ReactMic
        record={recording}
        className="sound-wave"
        onStop={onStop}
        strokeColor="#000000"
        backgroundColor="#FF4081"
      />
      <div>
        <button onClick={startRecording} disabled={recording}>
          Start Recording
        </button>
        <button onClick={stopRecording} disabled={!recording}>
          Stop Recording
        </button>
      </div>
      {blobURL && (
        <div>
          <h3>Recorded Audio:</h3>
          <audio controls src={blobURL}></audio>
        </div>
      )}
    </div>
  );
};

export default VoiceRecorder;
