import React from "react";

const Stat = (props) => {
  // Function to determine the color and label based on percentage
  const getColor = (percentage) => {
    if (percentage >= 75) return { color: 'text-green-500', label: 'GREEN' }; // High percentage
    if (percentage >= 50) return { color: 'text-yellow-500', label: 'YELLOW' }; // Medium percentage
    return { color: 'text-red-500', label: 'RED' }; // Low percentage
  };

  const colorInfo = getColor(props.percentage);

  return (
    <div className="h-[150px] w-1/4">
      <div className="w-full h-full bg-[#192533] rounded-3xl px-7 pt-6">
        <p className="text-center">{props.stat}</p>
        <div className="flex justify-between items-start text-xs">
          <p className={`pt-6 font-bold text-base ${colorInfo.color}`}>
            {/* {props.percentage} */}
            {Math.floor(props.percentage * 10) / 10}%
          </p>
          <div className="flex flex-col pt-4 text-slate-300">
            <p className={colorInfo.label === 'GREEN' ? 'text-green-500' : 'text-slate-300'}>GREEN</p>
            <p className={colorInfo.label === 'YELLOW' ? 'text-yellow-500' : 'text-slate-300'}>YELLOW</p>
            <p className={colorInfo.label === 'RED' ? 'text-red-500' : 'text-slate-300'}>RED</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Stat;
