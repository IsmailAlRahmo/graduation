import React, { useState, useEffect, useRef } from "react";
import { LineChart } from "@mui/x-charts";
import io from "socket.io-client";
import { useUser } from "../auth/useUser";

const Performance = ({ chartpoints }) => {
  // Ensure chartpoints is an array and format it correctly for the chart
  const formattedData = chartpoints?.map((point) => ({
    x: point.time, // x-axis (time)
    y: point.score, // y-axis (score)
  }));

  // Separate time and score for the x and y axes
  const timePoints = formattedData.map((point) => point.x);
  const performanceScores = formattedData.map((point) => point.y);
  return (
    <div className="w-3/6">
      <div className="w-full h-4/6 bg-[#192533] opacity-85 rounded-2xl flex flex-col">
        <h1 className="text-slate-200 font-thin text-center pt-4">
          Your performance chart{" "}
        </h1>
        <h1 className="text-slate-200 font-thin text-center">Advice & Notes</h1>

        <div className="w-full h-full px-4 py-4">
          <LineChart
            className="w-full h-full"
            grid={{ horizontal: true }}
            xAxis={[{ scaleType: "point", data: timePoints }]}
            series={[{ type: "line", data: performanceScores }]}
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
      <div className="text-white text-center pt-8 text-2xl h-2/6 ease-in-out">
        {/* Time spent: {seconds.length > 1 ? seconds.length - 1 : "0"} seconds */}
      </div>
    </div>
  );
};

export default Performance;
