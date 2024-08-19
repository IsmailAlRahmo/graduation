import { useNavigate } from "react-router-dom";
import thumbnail from "../assets/images/videoThmbnail.png";

const Video = ({ video }) => {

  const navigate = useNavigate();
  const getDescription = (score) => {
    if (score > 2) {
      return "Excellent session with high accuracy.";
    } else if (score > 1) {
      return "Good session, but there's room for improvement.";
    } else {
      return "Session needs improvement.";
    }
  };
  const handleViewClick = () => {
    navigate(`${video?.id}`);
  };
  return (
    <div className="w-full h-32 border-2 border-slate-300 rounded-2xl px-3 py-2 text-white">
      <div className="w-full h-full flex justify-start items-center">
        <img src={thumbnail} className="h-[140px]" alt="Video Thumbnail" />
        <div className="h-full w-full p-2">
          <div className="flex justify-between items-center w-2/6">
            <h2>{video?.video_name?.slice(0, 10)}</h2>
            <p className="text-slate-300 text-xs">
              {new Date(video?.recorded_at).toLocaleString()}
            </p>
          </div>
          <div className="text-sm h-10">
            <p className="text-ellipsis overflow-hidden h-full">
              {getDescription(video?.score)}
            </p>
          </div>
          <button
            onClick={handleViewClick}
            className="bg-[#0C5EA8] mt-1 w-16 p-1 rounded-lg text-white"
          >
            View
          </button>
        </div>
        <div className="h-full w-20 text-center pt-7 text-[#0C5EA8] font-bold">
          Rating
          <br />
          {video?.score.toFixed(1)}
        </div>
      </div>
    </div>
  );
};

export default Video;
