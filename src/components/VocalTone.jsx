import { Gauge, gaugeClasses } from "@mui/x-charts";
import { LinearProgress, linearProgressClasses } from "@mui/material";
import { styled } from "@mui/material/styles";
import React from "react";
import Emotion from "./Emotion";
import ImproveArea from "./ImproveArea";
import TopAreas from "./TopAreas";

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
    <div className="text-white pt-20 w-full">
      <div className=" flex h-44 pt-1 gap-2">
        <div className="pl-4 pt-4 w-2/4">
          <h1 className="text-5xl w-3/4 font-semibold text-[#F9F871]">
            Vocal tone score
          </h1>
        </div>

        <div className="w-1/2">
          <div className=" rounded-3xl bg-[#192533] w-full h-full flex items-center justify-center px-10">
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
                  stroke: "#F9F871",
                  transform: "translate(0px, 0px)",
                },
                [`& .${gaugeClasses.valueArc}`]: {
                  fill: "#F9F871",
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
      <div className=" w-full h-[435px] flex gap-2 py-2">
        <div className="bg-[#192533] pl-6 w-1/4 rounded-3xl pt-8">
          <p className="text-start w-28 text-lg">General emotion :</p>
          <div className="flex flex-col items-center pt-16 gap-3 font-semibold text-[#F9F871]">
            <p className=" text-2xl  text-center">HAPPY !</p>
            <p className=" text-2xl text-center">35%</p>
            <p className="text-sm px-2 text-white font-thin pt-8">
              "Your positive energy is infectious and can help engage your
              audience. Just make sure your happiness is appropriate for the
              topic of your speech."
            </p>
          </div>
        </div>
        <div className=" w-3/4 gap-5 flex flex-col pl-14">
          <div className="pb-4">
            <p className="text-start">Other emotions :</p>
          </div>
          <div className="flex justify-between w-full gap-5">
            <Emotion />
            <Emotion />
          </div>
          <div className="flex justify-between w-full gap-5">
            <Emotion />
            <Emotion />
          </div>
        </div>
      </div>
      <div className="w-full pt-3 flex gap-3 h-[120px]">
        <ImproveArea />
        <TopAreas />
      </div>
    </div>
  );
};

export default VocalTone;
