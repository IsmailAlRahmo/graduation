
import { Outlet } from "react-router-dom";
import NavBar from "./NavBar";

const Layout = () => {
  
  return (
    <div className="w-full h-screen bg-gradient-to-br from-[#2C2C2C] to-[#012C61] px-10 py-12">
      <div className="h-full w-full">
        <NavBar/>
        <div className="w-full h-full pt-4" id="children-container">
          <Outlet/>
        </div>
      </div>
    </div>
  );
};

export default Layout;
{
  /* <div className="bg-yellow-200 w-80 h-40">
              <div>
                <h1 className="text-5xl ">Your overall score</h1>
                <p className="text-sm inline-block mt-5">
                  Monday, 15 July 2024{" "}
                </p>
                <p className="text-sm inline-block pl-4">11:00 AM</p>
              </div>
            </div> */
}
