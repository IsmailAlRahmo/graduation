import React, { useState } from "react";
import { LineChart } from "@mui/x-charts/LineChart";
import { Gauge, gaugeClasses } from "@mui/x-charts";
import { Stack } from "@mui/material";

const Layout = () => {
  const xLabels = [
    "sesseion 1",
    "sesseion 2",
    "sesseion 3",
    "sesseion 4",
    "sesseion 5",
    "sesseion 6",
  ];
  return (
    <div className="w-full h-screen bg-gradient-to-br from-[#2C2C2C] to-[#012C61] px-10 py-12">
      <div className="h-full w-full">
        <div className="flex h-12">
          <div className="flex py-3 mr-2 w-4/5  bg-[#192533] opacity-50 rounded-3xl justify-between text-slate-300">
            <nav className="ml-10">Overview</nav>
            <nav>My Videos</nav>
            <nav>My report</nav>
            <nav className="mr-10">Start Recording</nav>
          </div>
          <div className="w-1/5 text-wrap flex flex-col justify-start text-slate-200 font-semibold pl-1">
            <h1 className="text-xl">Hi, Omama Ewer</h1>
            <p className="text-sm text-slate-300">omamaewer@gmail.com</p>
          </div>
        </div>
        <div className="w-full h-full p-4">
          <div className="grid grid-cols-12 grid-rows-3 gap-4 grid-flow-row h-full pr-2">
            <div className=" col-span-6">
              {" "}
              <div className="pl-8">
                <h1 className="text-5xl text-slate-200 font-semibold">
                  Your overall
                  <br />
                  score
                </h1>
                <p className="text-sm inline-block mt-5 text-slate-300">
                  Monday, 15 July 2024{" "}
                </p>
                <p className="text-sm inline-block pl-4 text-slate-300">
                  11:00 AM
                </p>
              </div>
            </div>
            <div className=" col-span-3 rounded-3xl bg-[#192533] ">
              <Gauge
                width={130}
                height={130}
                value={3}
                valueMax={5}
                className="mx-auto "
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
            <div className="bg-white col-span-3 rounded-3xl pl-4 py-1">
              <h1 className=" text-sm">Body language score:</h1>
              <div className="font-bold">
                <Gauge
                  width={130}
                  height={130}
                  value={3}
                  valueMax={5}
                  className="mx-auto"
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
            <div className=" col-span-9 row-span-2 rounded-3xl bg-[#192533] pb-14 w-full h-full">
              <h1 className="text-center pt-5 text-slate-300">
                Your trend chart
              </h1>

              <LineChart
                className="w-full h-full"
                grid={{ horizontal: true }}
                xAxis={[{ scaleType: "point", data: xLabels }]}
                series={[{ type: "line", data: [1.2, 4.4, 1.6, 2.5] }]}
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
            <div className="bg-[#192533] col-span-3 rounded-3xl pl-4 py-2 text-sm text-slate-300">
              <h1>Facial expressions score:</h1>
              <div>
                <Gauge
                  width={130}
                  height={130}
                  value={2}
                  valueMax={5}
                  className="mx-auto "
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
            <div className="bg-white col-span-3 rounded-3xl pl-4 py-2 text-sm">
             
              <h1 className=" text-sm"> Vocal tone score:</h1>
              <div className="font-bold">
                <Gauge
                  width={130}
                  height={130}
                  value={3}
                  valueMax={5}
                  className="mx-auto"
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
    </div>
  );
};

export default Layout;
{
  /* <div className="bg-yellow-200 w-80 h-40">
              <div>
                <h1 className="text-5xl ">Your overall score</h1>
                <p className="text-sm inline-block mt-5">
                  Monday, 15 July 2024{" "}
                </p>
                <p className="text-sm inline-block pl-4">11:00 AM</p>
              </div>
            </div> */
}
