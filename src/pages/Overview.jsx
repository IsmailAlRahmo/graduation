import { Gauge, gaugeClasses, LineChart } from "@mui/x-charts";
import { useUser } from "../auth/useUser";
import { useEffect, useState } from "react";

const Overview = () => {
  const { user } = useUser();
  const [stats, setStats] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [currentDate, setCurrentDate] = useState("");
  const [currentTime, setCurrentTime] = useState("");

  useEffect(() => {
    const date = new Date();

    // Format the date: "Monday, 15 July 2024"
    const options = {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    };
    const formattedDate = date.toLocaleDateString("en-US", options);

    // Format the time: "11:00 AM"
    const hours = date.getHours();
    const minutes = date.getMinutes();
    const formattedTime = `${hours % 12 || 12}:${
      minutes < 10 ? "0" : ""
    }${minutes} ${hours < 12 ? "AM" : "PM"}`;

    setCurrentDate(formattedDate);
    setCurrentTime(formattedTime);
  }, []);
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5001/average_score", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "User-ID": user.id, // Custom header to send the user ID
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch stats");
        }

        const data = await response.json();
        setStats(data);
      } catch (error) {
        console.error("Error fetching stats:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchStats();
  }, [user.id]);

  // const date = new Date();

  // Prepare data for the chart
  const xLabels =
    stats?.video_details?.map((video) => video.video_name.slice(0, 10)) || [];
  const scores =
    stats?.video_details?.map((video) =>
      parseFloat(video.final_score.toFixed(1))
    ) || [];

  return (
    <div>
      <div className=" w-full pt-6 flex">
        <div className="h-40 w-[834px]  flex justify-between items-center">
          <div className="pl-12 ">
            <h1 className="text-5xl text-slate-200 font-semibold">
              Your overall
              <br />
              score
            </h1>
            <p className="text-sm inline-block mt-5 text-slate-300">
              {currentDate}
            </p>
            <p className="text-sm inline-block pl-4 text-slate-300">
              {currentTime}
            </p>
          </div>
          <div className="rounded-3xl bg-[#192533] py-2 w-[250px] h-[170px]">
            <Gauge
              value={!isLoading ? parseInt(parseFloat(stats?.average_score?.toFixed(1))) : 0}
              valueMax={5}
              className=" w-[250px] h-[130px]"
              innerRadius="75%"
              outerRadius="100%"
              sx={{
                [`& .${gaugeClasses.valueText}`]: {
                  fontSize: 18,
                  stroke: "#FFFFFF",
                  transform: "translate(0px, 0px)",
                },
                [`& .${gaugeClasses.referenceArc}`]: {
                  fill: "#FFFFFF",
                },
              }}
              text={({ value, valueMax }) => `${value} / ${valueMax}`}
            />
            <p className="text-center text-slate-200">NICE SHOW!</p>
          </div>
        </div>

        <div className="font-bold w-[250px] h-[160px] bg-[#dadee2] rounded-3xl ml-5">
          <p className="text-sm ml-4 pt-2">Body language score:</p>
          <Gauge
            value={!isLoading ? parseInt(parseFloat(stats?.average_score?.toFixed(1))) : 0}
            valueMax={5}
            className="w-[250px] h-[130px]"
            innerRadius="75%"
            outerRadius="100%"
            sx={{
              [`& .${gaugeClasses.valueText}`]: {
                fontSize: 18,
                transform: "translate(0px, 0px)",
              },
              [`& .${gaugeClasses.referenceArc}`]: {
                fill: "#FFFFFF",
              },
            }}
            text={({ value, valueMax }) => `${value} / ${valueMax}`}
          />
        </div>
      </div>
      <div className="w-full h-[326px] flex">
        <div className=" h-full w-[834px] pb-1 pt-3">
          <div className="rounded-3xl bg-[#192533] pb-16 w-full h-full">
            <h1 className="text-center pt-5 text-slate-300">
              Your trend chart
            </h1>

            <LineChart
              className="w-full h-full"
              grid={{ horizontal: true }}
              xAxis={[{ scaleType: "point", data: xLabels }]}
              yAxis={[{ min: 0, max: 5 }]} // Set Y-axis range from 0 to 5
              series={[{ type: "line", data: scores }]}
              sx={{
                "& .MuiChartsAxis-left .MuiChartsAxis-line": {
                  stroke: "#94a3b8",
                },
                "& .MuiChartsAxis-left .MuiChartsAxis-tick": {
                  stroke: "#94a3b8",
                },
                "& .MuiChartsAxis-left": {
                  stroke: "#94a3b8",
                },
                "& .MuiChartsAxis-bottom .MuiChartsAxis-line ": {
                  stroke: "#94a3b8",
                },
                "& .MuiChartsAxis-bottom .MuiChartsAxis-tick": {
                  stroke: "#94a3b8",
                },
                "& .MuiChartsAxis-bottom": {
                  stroke: "#94a3b8",
                },
                "& .MuiChartsGrid-line": {
                  stroke: "#94a3b8",
                },
              }}
            />
          </div>
        </div>
        <div className=" pl-4 pt-3">
          <div className=" rounded-3xl bg-[#192533] mx-auto">
            <h1 className=" text-sm ml-4 pt-2 text-slate-200">
              Facial expressions score:
            </h1>
            <div className="">
              <Gauge
                value={!isLoading ? 3 : 0} // Placeholder value for facial expressions score
                valueMax={5}
                className=" w-[250px] h-[120px]"
                innerRadius="75%"
                outerRadius="100%"
                sx={{
                  [`& .${gaugeClasses.valueText}`]: {
                    fontSize: 18,
                    stroke: "#FFFFFF",
                    transform: "translate(0px, 0px)",
                  },
                  [`& .${gaugeClasses.referenceArc}`]: {
                    fill: "#FFFFFF",
                  },
                }}
                text={({ value, valueMax }) => `${value} / ${valueMax}`}
              />
            </div>
          </div>
          <div className="bg-[#dadee2] rounded-3xl text-sm mt-3">
            <h1 className=" text-sm ml-4 pt-2">Vocal tone score:</h1>
            <div className="font-bold mx-auto">
              <Gauge
                value={!isLoading ? 4 : 0} // Placeholder value for vocal tone score
                valueMax={5}
                className="w-[250px] h-[120px]"
                innerRadius="75%"
                outerRadius="100%"
                sx={{
                  [`& .${gaugeClasses.valueText}`]: {
                    fontSize: 18,
                    transform: "translate(0px, 0px)",
                  },
                  [`& .${gaugeClasses.referenceArc}`]: {
                    fill: "#FFFFFF",
                  },
                }}
                text={({ value, valueMax }) => `${value} / ${valueMax}`}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Overview;
