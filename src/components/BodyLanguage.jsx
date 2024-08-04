import { Gauge, gaugeClasses } from "@mui/x-charts";
import React from "react";
import Stat from "./Stat";

const BodyLanguage = () => {
  return (
    <div className=" text-white">
      <div className="w-full h-44 flex gap-2 pt-1">
        <div className="pl-16 w-1/4">
          <p className="text-md text-gray-400">Recent report</p>
          <h1 className="text-5xl w-1/2 font-bold text-[#25AB89]">
            Body language score
          </h1>
        </div>
        <div className="w-2/4 py-1">
          <div className=" rounded-3xl bg-[#192533] w-full h-full flex items-center justify-center px-20">
            <p className="text-2xl font-thin text-white">NICE SHOW!</p>
            <Gauge
              value={2.4}
              valueMax={5}
              className=""
              innerRadius="75%"
              outerRadius="100%"
              sx={{
                [`& .${gaugeClasses.valueText}`]: {
                  fontSize: 18,
                  stroke: "#25AB89",
                  transform: "translate(0px, 0px)",
                },
                [`& .${gaugeClasses.valueArc}`]: {
                  fill: "#25AB89",
                },
                [`& .${gaugeClasses.referenceArc}`]: {
                  fill: "#FFFFFF",
                },
              }}
              text={({ value, valueMax }) => `${value} / ${valueMax}`}
            />
          </div>
        </div>
        <div className=" w-1/4 py-2">
          <div className="w-full h-full bg-[#192533] flex flex-col gap-3 px-5 py-5 rounded-3xl text-slate-300">
            <p>Timing:</p>
            <p>Monday, 15 July 2024 </p>
            <p>11:00 AM</p>
          </div>
        </div>
      </div>
      <div className="w-full flex gap-2 pt-2">
        <Stat stat="Opened hands" />
        <Stat stat="Straight hands" />
        <Stat stat="Wrist closed" />
        <Stat stat="Straight standing" />
      </div>
      <div className="w-full  flex gap-2 pt-2">
        <Stat stat="Hands crossed" />
        <Stat stat="Hands on waist" />
        <Stat stat="Not straight" />
        <Stat stat="Hands on head" />
      </div>
      <div className="w-full pt-2 flex gap-2 h-[97px]">
        <div className="w-1/2 bg-[#192533] pt-2 rounded-3xl ">
          <p className="text-center"> Your top areas:</p>
        </div>
        <div className="w-1/2 bg-[#192533] pt-2 rounded-3xl">
          <p className="text-center"> Your areas to improve:</p>
        </div>
      </div>
    </div>
  );
};

export default BodyLanguage;
