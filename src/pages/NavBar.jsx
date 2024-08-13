import { NavLink } from "react-router-dom";
import { FaCircle } from "react-icons/fa";
import { IoMdRadioButtonOn } from "react-icons/io";
import { useUser } from "../auth/useUser";
const NavBar = () => {
  const user = useUser();
  return (
    <div className="flex items-center justify-between pt-10">
      <div className="flex items-center h-12 mr-2 w-3/4 bg-[#192533] opacity-85 rounded-full justify-between text-white text-xl font-extralight">
        <nav className=" pl-4">
          <NavLink
            to={"overview"}
            className={({ isActive }) =>
              "flex items-center " + (isActive ? " active" : "")
            }
          >
            {({ isActive }) => (
              <>
                {
                  <FaCircle
                    className={`text-xs ${!isActive ? "invisible" : ""}`}
                  />
                }
                <span className="pl-2">Overview</span>
              </>
            )}
            {/* <span className="pl-2">Overview</span> */}
          </NavLink>
        </nav>
        <nav>
          <NavLink
            to={"videos"}
            className={({ isActive }) =>
              "flex items-center " + (isActive ? " active" : "")
            }
          >
            {({ isActive }) => (
              <>
                <FaCircle
                  className={`text-xs ${!isActive ? "invisible" : ""}`}
                />
                <span className="pl-2">Videos</span>
              </>
            )}
          </NavLink>
        </nav>
        <nav>
          {" "}
          <NavLink
            to={"reports"}
            className={({ isActive }) =>
              "flex items-center" + (isActive ? " active" : "")
            }
          >
            {({ isActive }) => (
              <>
                <FaCircle
                  className={`text-xs ${!isActive ? "invisible" : ""}`}
                />
                <span className="pl-2">Reports</span>
              </>
            )}
          </NavLink>
        </nav>
        <nav className="mr-10">
          <NavLink
            to={"record"}
            className={({ isActive }) =>
              "flex items-center" + (isActive ? " active" : "")
            }
          >
            {({ isActive }) => (
              <>
                <IoMdRadioButtonOn
                  className={`text-xs ${!isActive ? "invisible" : ""}`}
                />

                <span className="pl-2">Start Recording</span>
              </>
            )}
          </NavLink>
        </nav>
      </div>
      <div className="w-1/4 pl-8 text-wrap flex flex-col justify-start text-slate-200 font-semibold">
        <h1 className="text-xl">Hi, {user?.user?.username}</h1>
        <p className="text-sm text-slate-300">{user?.user?.email}</p>
      </div>
    </div>
  );
};

export default NavBar;
