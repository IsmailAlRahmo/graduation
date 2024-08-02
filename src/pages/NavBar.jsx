import React from "react";
import { Link } from "react-router-dom";

const NavBar = () => {
  return (
    <div className="flex h-12">
      <div className="flex py-3 mr-2 w-4/5  bg-[#192533] opacity-50 rounded-3xl justify-between text-slate-300">
        <nav className="ml-10">
          <Link to={'overview'}>Overview</Link>
        </nav>
        <nav> <Link to={'videos'}>My Videos</Link></nav>
        <nav> <Link to={'reports'}>My report</Link></nav>
        <nav className="mr-10">Start Recording</nav>
      </div>
      <div className="w-1/5 text-wrap flex flex-col justify-start text-slate-200 font-semibold pl-1">
        <h1 className="text-xl">Hi, Omama Ewer</h1>
        <p className="text-sm text-slate-300">omamaewer@gmail.com</p>
      </div>
    </div>
  );
};

export default NavBar;
