import { Gauge, gaugeClasses } from "@mui/x-charts";
import { LinearProgress, linearProgressClasses } from "@mui/material";
import { styled } from "@mui/material/styles";
import React from "react";
import sad from "../assets/emojies/sad.png";
import angry from "../assets/emojies/angry.png";
import fear from "../assets/emojies/fear.png";
import happy from "../assets/emojies/happy.png";
import calm from "../assets/emojies/calm.png";
import Emotion from "./Emotion";
const VocalTone = () => {
  let mycolor = "#8CD67C";
  const BorderLinearProgress = styled(LinearProgress)(({ theme }) => ({
    height: 5,
    borderRadius: 5,
    [`&.${linearProgressClasses.colorPrimary}`]: {
      backgroundColor:
        theme.palette.grey[theme.palette.mode === "light" ? 200 : 800],
    },
    [`& .${linearProgressClasses.bar}`]: {
      borderRadius: 5,
      backgroundColor: theme.palette.mode === "light" ? mycolor : "#308fe8",
    },
  }));
  return (
    <div className="text-white">
      <div className="w-full flex h-44 pt-1 gap-2">
        <div className="pl-16 pt-4 w-2/4">
          <h1 className="text-5xl w-2/4 font-bold text-[#8CD67C]">
            Vocal tone score
          </h1>
        </div>

        <div className="w-1/2">
          <div className=" rounded-3xl bg-[#192533] w-full h-full flex items-center justify-center px-20">
            <p className="text-3xl font-thin text-white">fabulous show!</p>
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
                  fill: "#8CD67C",
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
      <div className=" w-full h-64  flex gap-2 py-2">
        <div className="bg-[#192533] w-2/6  rounded-3xl pt-4">
          <p className="text-start pl-4 text-sm">General emotion : </p>
          <div className="flex flex-col items-center pt-4 gap-3">
            <p className="font-bold text-2xl text-center">Happy!</p>
            <p className="font-bold text-2xl text-center">35%</p>
            <p className="text-sm px-3">
              "Your positive energy is infectious and can help engage your
              audience. Just make sure your happiness is appropriate for the
              topic of your speech."
            </p>
          </div>
        </div>
        <div className=" w-4/6 h-64 gap-2 flex flex-col pl-10">
          <div className="">
            <p className="text-start">Negative facial emotions:</p>
          </div>
          <div className="flex justify-between w-full  ">
            <Emotion />
            <Emotion />
          </div>
          <div className="flex justify-between w-full  ">
            <Emotion />
            <Emotion />
          </div>
          {/* <div className="flex justify-between w-full bg-red-400 ">
            <div className="w-2/6 h-[120px] bg-yellow-300"></div>
            <div className="w-2/6 h-[120px] bg-yellow-300"></div>
          </div>
          <div className="flex justify-between w-full bg-red-400 h-full">
            <div className="w-2/6 h-[120px] bg-yellow-300"></div>
            <div className="w-2/6 h-[120px] bg-yellow-300"></div>
          </div> */}
        </div>
      </div>
      <div className="w-full h-[97px]  flex gap-1">
        <div className="w-1/2 bg-[#192533] pt-1 rounded-3xl">
          <p className="text-center"> Your top areas:</p>
        </div>
        <div className="w-1/2 bg-[#192533] pt-1 rounded-3xl">
          <p className="text-center"> Your areas to improve:</p>
        </div>
      </div>
    </div>
  );
};

export default VocalTone;
