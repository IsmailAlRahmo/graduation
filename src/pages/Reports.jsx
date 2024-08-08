import { Gauge, gaugeClasses } from "@mui/x-charts";
import React from "react";
import Stat from "../components/Stat";
import BodyLanguage from "../components/BodyLanguage";
import FacialExpressions from "../components/FacialExpressions";
import VocalTone from "../components/VocalTone";

const Reports = () => {
  return (
    <div className="w-full h-[529px] overflow-y-scroll no-scrollbar ">
      <BodyLanguage />
      <FacialExpressions />
      <VocalTone />
    </div>
  );
};

export default Reports;
