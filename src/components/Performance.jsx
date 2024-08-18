import React, { useState, useEffect, useRef } from "react";
import { LineChart } from "@mui/x-charts";
import io from "socket.io-client";
import { useUser } from "../auth/useUser";

const Performance = ({ chartpoints }) => {
  
  return (
    <div className="w-3/6">
      <div className="w-full h-4/6 bg-[#192533] opacity-85 rounded-2xl flex flex-col">
        <h1 className="text-slate-200 font-thin text-center pt-4">
          Your performance chart{" "}
        </h1>
        <h1 className="text-slate-200 font-thin text-center">Advice & Notes</h1>
        <ul className="text-slate-300 font-light text-center">
          {/* {chartpoints.map((message, index) => (
            <li key={index}>{message}</li>
          ))} */}
        </ul>
        {/* <div className="w-full h-full px-4 py-4">
          <LineChart
            className="w-full h-full"
            grid={{ horizontal: true }}
            xAxis={[{ scaleType: "point", data: seconds }]}
            series={[{ type: "line", data: data }]}
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
        </div> */}
      </div>
      <div className="text-white text-center pt-8 text-2xl h-2/6 ease-in-out">
        {/* Time spent: {seconds.length > 1 ? seconds.length - 1 : "0"} seconds */}
      </div>
    </div>
  );
};

export default Performance;
