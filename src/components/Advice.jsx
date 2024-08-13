import React, { useState, useEffect } from "react";

// eslint-disable-next-line react/prop-types
const Advice = ({ recording }) => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    if (recording) {
      const interval = setInterval(() => {
        const newMessage = `Message ${Math.floor(Math.random() * 100)}`;
        setMessages((prevMessages) => [...prevMessages, newMessage]);
      }, 3000);

      // Clear the interval when recording stops
      return () => clearInterval(interval);
    }
  }, [recording]);

  return (
    <div className="w-5/12 h-full bg-[#192533] opacity-85 rounded-2xl overflow-y-scroll">
      <div className="pt-4">
        <h1 className="text-slate-200 font-thin text-center">
          Your advices & notes
        </h1>
        <ul className="text-slate-300 font-light text-center ">
          {messages.map((message, index) => (
            <li key={index}>{message}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Advice;
