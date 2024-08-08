import { Outlet } from "react-router-dom";
import NavBar from "./NavBar";

const Layout = () => {
  return (
    <div className="w-full h-full bg-gradient-to-br from-[#2C2C2C] to-[#012C61] px-44">
      <NavBar />
      <div className="">
        <Outlet />
      </div>
    </div>
  );
};

export default Layout;
