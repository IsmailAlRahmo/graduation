import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import thumbnail from "../assets/images/videoThmbnail.png";
import { useUser } from "../auth/useUser";
import Reports from './Reports';
const VideoDetail = () => {
  const { id } = useParams(); // Get the video ID from the URL
  const [video, setVideo] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const { user } = useUser();
  useEffect(() => {
    const fetchVideoDetail = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5001/video/${id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'User-ID': user.id, // Replace with actual user ID if needed
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch video details');
        }

        const data = await response.json();
        console.log(data);
        
        setVideo(data);
      } catch (error) {
        console.error('Error fetching video details:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchVideoDetail();
  }, [id]);

  if (isLoading) {
    return <p>Loading...</p>;
  }

  if (!video) {
    return <p>Video not found</p>;
  }

  return (
    <Reports id={id}/>
  );
};

export default VideoDetail;
