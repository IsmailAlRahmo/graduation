
import thumbnail from "../assets/images/videoThmbnail.png";

const Video = ({video}) => {
  // console.log(video);
  
  return (
    <div className="w-full h-32 border-2  border-slate-300 rounded-2xl px-3 py-2 text-white">
      <div className="w-full h-full flex justify-start items-center">
        <img src={thumbnail} className="h-[140px]" />
        <div className="h-full w-full p-2 ">
          <div className="flex justify-between items-center w-2/6 ">
            <h2>{video?.title}</h2>
            <p className="text-slate-300 text-xs">
              Saturday, 13 July 2024 9:00 AM{" "}
            </p>
          </div>
          <div className="text-sm h-10 ">
            <p className="text-ellipsis overflow-hidden h-full">
              {video?.description}
            </p>
          </div>
          <button className="bg-[#0C5EA8] mt-1 w-16 p-1 rounded-lg text-white">
            View
          </button>
        </div>
        <div className=" h-full w-20 text-center pt-7 text-[#0C5EA8] font-bold">
          Rating
          <br />
          {video?.score}
        </div>
      </div>
    </div>
  );
};

export default Video;
