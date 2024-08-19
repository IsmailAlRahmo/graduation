import { useEffect, useState } from "react";
import BodyLanguage from "../components/BodyLanguage";
import FacialExpressions from "../components/FacialExpressions";
import VocalTone from "../components/VocalTone";
import { useUser } from "../auth/useUser";
import { useParams } from "react-router-dom";

const Reports = () => {
  const { id } = useParams(); // Get the video ID from the URL
  const { user } = useUser();
  const [isLoading, setIsLoading] = useState(true);
  const [report, setReport] = useState(null);
  const [latestVideo, setLatestVideo] = useState(null);

  useEffect(() => {
    const fetchReport = async (videoId) => {
      try {
        const response = await fetch(
          `http://127.0.0.1:5001/report/${videoId}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "User-ID": user.id, // Custom header to send the user ID
            },
          }
        );

        if (!response.ok) {
          throw new Error("Failed to fetch report");
        }

        const data = await response.json();
        console.log('report data',data);
        
        setReport(data);
      } catch (error) {
        console.error("Error fetching report:", error);
      } finally {
        setIsLoading(false);
      }
    };

    const fetchLatestVideo = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5001/video/latest", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "User-ID": user.id, // Custom header to send the user ID
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch latest video");
        }

        const data = await response.json();
        setLatestVideo(data);
        console.log(data);
        
        return data.id;
      } catch (error) {
        console.error("Error fetching latest video:", error);
        return null;
      }
    };

    const getReport = async () => {
      let videoId = id; // Default to URL parameter

      if (!videoId) {
        videoId = await fetchLatestVideo(); // Fetch latest video if no ID in URL
      }

      if (videoId) {
        console.log('video id passed',videoId);
        
        fetchReport(videoId);
      } else {
        setIsLoading(false); // No ID available, stop loading
      }
    };

    getReport();
  }, [id, user.id]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="w-full h-[529px] overflow-y-scroll no-scrollbar">
      {/* Render the report components with the fetched data */}
      {report && (
        <>
          <BodyLanguage report={report} />
          {/* <FacialExpressions report={report.facialExpressions} /> */}
          {/* <VocalTone report={report.vocalTone} /> */}
        </>
      )}
    </div>
  );
};

export default Reports;
