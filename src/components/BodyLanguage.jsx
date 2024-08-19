import React, { useEffect, useState } from "react";
import { Gauge, gaugeClasses } from "@mui/x-charts";
import Stat from "./Stat";
import ImproveArea from "./ImproveArea";
import TopAreas from "./TopAreas";
import { useUser } from "../auth/useUser";

const BodyLanguage = ({report}) => {
  return (
    <div className="w-full pt-4 text-white">
      <div className="flex w-full h-56 gap-3">
        <div className="w-3/4 flex justify-between">
          <div className="w-1/3 pl-4">
            <p className="text-md text-gray-400">Recent report</p>
            <h1 className="text-5xl w-1/2 font-semibold text-[#25AB89]">
              Body language score
            </h1>
          </div>
          <div className="w-2/3">
            <div className="rounded-3xl bg-[#192533] w-full h-full flex items-center justify-center px-14 py-4">
              <p className="text-2xl font-thin text-white">
                {report.evaluation}
              </p>
              <Gauge
                value={Math.floor(report.final_score * 10) / 10}
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
            <p>{report.start_time.split(" ")[0]}</p>
            <p>
              {report.start_time.split(" ")[1]}{" "}
              {report.start_time.split(" ")[2]}
            </p>
          </div>
        </div>
      </div>

      <div className="w-full flex gap-3 pt-3 ">
        <Stat
          stat="Opened hands"
          percentage={report.open_palms_forward_percentage}
        />
        <Stat
          stat="Straight hands"
          percentage={report.hand_straight_down_percentage}
        />
        <Stat stat="Wrist closed" percentage={report.hand_crossed_percentage} />
        <Stat
          stat="Straight standing"
          percentage={report.standing_straight_percentage}
        />
      </div>
      <div className="w-full flex gap-3 pt-3">
        <Stat
          stat="Hands crossed"
          percentage={report.hand_crossed_percentage}
        />
        <Stat
          stat="Hands on waist"
          percentage={report.hand_on_waist_percentage}
        />
        <Stat stat="Not straight" percentage={report.body_lean_percentage} />
        <Stat
          stat="Hands on head"
          percentage={report.hand_on_head_percentage}
        />
      </div>
      <div className="w-full pt-3 flex gap-3 h-[120px]">
        <TopAreas tips={report.positive_tips} />
        <ImproveArea tips={report.negative_tips} />
      </div>
    </div>
  );
};

export default BodyLanguage;
