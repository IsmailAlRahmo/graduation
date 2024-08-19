import { useQuery } from "react-query";
const fetchVideos = async (userId) => {
  
  const response = await fetch("http://127.0.0.1:5001/videos", {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'User-ID': userId, // Custom header to send the user ID
    },
    // credentials: 'include', // Include credentials if needed
  });
  if (!response.ok) {
    throw new Error("Failed to fetch Videos", response);
  }
  return await response.json();
};
export const useVideos = (id) => {
  const { data: videos = [], isLoading } = useQuery(["videos", id], () => fetchVideos(id), {
    // refetchInterval: 1000,
    refetchOnWindowFocus: false,
    retry: 2,
  });

  return {
    videos,
    isLoading,
  };
};
