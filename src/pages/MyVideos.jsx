import Video from "../components/Video";

const MyVideos = () => {
  return (
    <div className="w-full h-full py-2 flex flex-col gap-5 pr-16">
      <div className="flex justify-between items-center w-full text-slate-300">
        <h1 className="text-5xl  ">Your videos list</h1>
        <p className="">Last upload was on: 26 July 2024</p>
      </div>
      <div className="flex flex-col gap-2  py-1 overflow-y-scroll no-scrollbar"> 
        
        <Video/>
        <Video/>
        <Video/>
        <Video/>
        <Video/>
      </div>
    </div>
  );
};

export default MyVideos;
