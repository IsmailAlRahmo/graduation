import React, { useState, useEffect, useRef } from "react";

const Advice = ({ feedback }) => {
  
  return (
    <div className="w-5/12 h-full bg-[#192533] opacity-85 rounded-2xl overflow-y-scroll no-scrollbar">
      <div className="pt-4">
        <h1 className="text-slate-200 font-thin text-center">Advice & Notes</h1>
        <ul className="text-slate-300 font-light text-center">
          {feedback.map((message, index) => (
            <li key={index}>{message}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Advice;
