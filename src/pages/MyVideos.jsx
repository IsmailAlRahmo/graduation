import { useEffect, useState } from "react";
import Video from "../components/Video";
import { useUser } from "../auth/useUser";

const MyVideos = () => {
  const { user } = useUser();
  const [videos, setVideos] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchVideos = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5001/videos", {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'User-ID': user.id, // Custom header to send the user ID
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch Videos");
        }

        const data = await response.json();
        console.log(data);
        
        setVideos(data);
      } catch (error) {
        console.error("Error fetching videos:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchVideos();
  }, []);

  return (
    <div className="py-2 flex flex-col gap-5">
      <div className="flex justify-between items-end w-full text-slate-300">
        <h1 className="text-5xl pl-16">Your videos list</h1>
        <p className="">Last upload was on: 26 July 2024</p>
      </div>
      {!isLoading && (
        <div className="flex flex-col gap-2 h-[400px] mt-1 overflow-y-scroll no-scrollbar">
          {videos.map((video, index) => (
            <Video key={index} video={video} />
          ))}
        </div>
      )}
    </div>
  );
};

export default MyVideos;
