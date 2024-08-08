import { Gauge, gaugeClasses } from "@mui/x-charts";
import React from "react";
import Stat from "./Stat";
import ImproveArea from "./ImproveArea";
import TopAreas from "./TopAreas";

const BodyLanguage = () => {
  return (
    <div className="w-full pt-4 text-white  ">
      <div className="flex w-full  h-56 gap-3">
        <div className="w-3/4  flex justify-between">
          <div className="w-1/3 pl-4">
            <p className="text-md text-gray-400">Recent report</p>
            <h1 className="text-5xl w-1/2  font-semibold text-[#25AB89]">
              Body language score
            </h1>
          </div>
          <div className="w-2/3">
            <div className=" rounded-3xl bg-[#192533] w-full h-full flex items-center justify-center px-14 py-4">
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
        </div>
        <div className="w-1/4 pl-1">
          <div className="w-full h-full bg-[#192533] flex flex-col gap-3 px-5 py-14 rounded-3xl text-slate-300">
            <p>Timing:</p>
            <p>Monday, 15 July 2024 </p>
            <p>11:00 AM</p>
          </div>
        </div>
      </div>

      <div className="w-full flex gap-3 pt-3 ">
        <Stat stat="Opened hands" />
        <Stat stat="Straight hands" />
        <Stat stat="Wrist closed" />
        <Stat stat="Straight standing" />
      </div>
      <div className="w-full flex gap-3 pt-3">
        <Stat stat="Hands crossed" />
        <Stat stat="Hands on waist" />
        <Stat stat="Not straight" />
        <Stat stat="Hands on head" />
      </div>
      <div className="w-full pt-3 flex gap-3 h-[120px]">
        <ImproveArea />
        <TopAreas />
      </div>
    </div>
  );
};

export default BodyLanguage;
