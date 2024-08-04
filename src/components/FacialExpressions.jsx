import { LinearProgress, linearProgressClasses } from "@mui/material";
import { Gauge, gaugeClasses } from "@mui/x-charts";
import { styled } from "@mui/material/styles";
import React from "react";
import sad from "../assets/emojies/sad.png";
import angry from "../assets/emojies/angry.png";
import fear from "../assets/emojies/fear.png";
import happy from "../assets/emojies/happy.png";
import calm from "../assets/emojies/calm.png";

const FacialExpressions = () => {
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
    <div className=" text-white">
      <div className="w-full flex h-44 pt-1 gap-2">
        <div className="pl-16 pt-4 w-2/4">
          <h1 className="text-5xl w-1/2 font-bold text-[#8CD67C]">
            Facial expressions score
          </h1>
        </div>

        <div className="w-1/2">
          <div className=" rounded-3xl bg-[#192533] w-full h-full flex items-center justify-center px-20">
            <p className="text-3xl font-thin text-white">NICE SHOW!</p>
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
      <div className=" w-full h-64 flex gap-2 py-2">
        <div className="bg-[#192533] w-1/2 h-full rounded-3xl pt-4">
          <p className="text-center">Positive facial emotions:</p>
          <div className="flex justify-between items-center px-32 py-4">
            <div>
              <div className="flex flex-col gap-3 items-center">
                <h1 className="text-[#8CD67C]">Happy</h1>
                <img src={happy} alt="" width={40} height={40} />
                <BorderLinearProgress
                  variant="determinate"
                  value={70}
                  className="w-20"
                />
                <p className="text-[#8CD67C]">70%</p>
              </div>
            </div>
            <div>
              <div>
                <div className="flex flex-col gap-3 items-center">
                  <h1 className="text-[#8CD67C]">Calm</h1>
                  {/* <RiEmotionHappyLine className="text-4xl " /> */}
                  <img src={calm} alt="" width={40} height={40} />
                  <BorderLinearProgress
                    variant="determinate"
                    value={40}
                    className="w-20"
                  />
                  <p className="text-[#8CD67C]">40%</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="bg-[#192533] w-1/2 h-full rounded-3xl pt-4">
          <p className="text-center">Negative facial emotions:</p>
          <div className="flex justify-between items-center px-32 py-4">
            <div>
              <div className="flex flex-col gap-3 items-center">
                <h1 className="text-[#8CD67C]">Sad</h1>
                <img src={sad} alt="" width={40} height={40} />
                <BorderLinearProgress
                  variant="determinate"
                  value={70}
                  className="w-20"
                />
                <p className="text-[#8CD67C]">70%</p>
              </div>
            </div>
            <div>
              <div>
                <div className="flex flex-col gap-3 items-center">
                  <h1 className="text-[#8CD67C]">Fearful</h1>
                  <img src={fear} width={40} height={40} alt="" className="" />
                  <BorderLinearProgress
                    variant="determinate"
                    value={40}
                    className="w-20"
                  />
                  <p className="text-[#8CD67C]">40%</p>
                </div>
              </div>
            </div>
            <div>
              <div>
                <div className="flex flex-col gap-3 items-center">
                  <h1 className="text-[#8CD67C]">Angry</h1>
                  {/* <RiEmotionHappyLine className="text-4xl " /> */}
                  <img src={angry} alt="" width={40} height={40} />
                  <BorderLinearProgress
                    variant="determinate"
                    value={40}
                    className="w-20"
                  />
                  <p className="text-[#8CD67C]">40%</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="w-full h-[97px] flex gap-1">
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

export default FacialExpressions;
