import React from "react";

const Stat = (props) => {
  return (
    <div className=" h-[150px] w-1/4">
      <div className="w-full h-full bg-[#192533] rounded-3xl px-7 pt-6">
        <p className="text-center">{props.stat}</p>
        <div className="flex justify-between items-start text-xs">
          <p className="pt-6 font-bold text-base">80%</p>
          <div className="flex flex-col pt-4 text-slate-300">
            <p className="">GREEN</p>
            <p className="">YELLOW</p>
            <p className="">RED</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Stat;
