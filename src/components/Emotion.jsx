import { LinearProgress, linearProgressClasses } from "@mui/material";
import { styled } from "@mui/material/styles";
import React from "react";

const Emotion = () => {
  let mycolor = "#F9F871";
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
    <div className="w-3/6 h-[170px] rounded-3xl bg-[#192533]">
      <div className="flex flex-col gap-7 items-center pt-8 text-[#F9F871]">
        <h1 className="">Happy</h1>

        <BorderLinearProgress
          variant="determinate"
          value={70}
          className="w-32"
        />
        <p className="">70%</p>
      </div>
    </div>
  );
};

export default Emotion;
