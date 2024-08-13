import { useQuery } from "react-query";
const fetchVideos = async () => {
  const response = await fetch("http://localhost:3000/videos");
  if (!response.ok) {
    throw new Error("Failed to fetch Videos", response);
  }
  return await response.json();
};
export const useVideos = () => {
  const { data: videos = [], isLoading } = useQuery(["videos"], fetchVideos, {
    // refetchInterval: 1000,
    refetchOnWindowFocus: false,
    retry: 2,
  });

  return {
    videos,
    isLoading,
  };
};
