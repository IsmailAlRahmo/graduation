import { FaPlayCircle } from "react-icons/fa";
import Advice from "../components/Advice";
import Performance from "../components/Performance";
import VideoOverlayComponent from "../components/live-video/VideoOverlayComponent";
import { FaPause } from "react-icons/fa";
import { useState } from "react";
const Live = () => {
  const [recording, setRecording] = useState(0);
  return (
    <div className="w-full h-screen bg-black px-24 py-20 ">
      <div className="w-full h-full flex justify-evenly">
        <Advice recording={recording} />
        {/* <Performance recording={recording} /> */}
        {/* <VideoOverlayComponent /> */}
      </div>
      <div className="text-center  flex justify-center">
        <button onClick={() => setRecording(!recording)}>
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
