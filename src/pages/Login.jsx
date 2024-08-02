import { Link } from "react-router-dom";
import amico from "../assets/images/amico.svg";
const Login = () => {
  return (
    <div className="w-full h-screen bg-gradient-to-br from-[#2C2C2C] to-[#012C61]">
      <div className=" w-full h-full flex flex-row justify-between items-center py-32 px-20">
        <div className="w-1/2 h-full flex flex-col pt-2 px-20 gap-6">
          <h1 className="text-3xl tracking-wider text-slate-300 text-center mb-5">
            Welcome back !
          </h1>
          <form className="pt-10 flex flex-col gap-10 text-slate-200 w-full ">
            <input
              type="text"
              placeholder="E-mail Address"
              className=" h-14 bg-[#192535] pl-8 rounded-3xl focus:outline-none"
            />
            <div className="flex flex-col">
              <input
                type="password"
                placeholder="Password"
                className=" h-14 bg-[#192535] pl-8 rounded-3xl focus:outline-none mb-3"
              />
              <Link
                to={"/reset-password"}
                className="text-[#0066A4] pl-2 text-sm"
              >
                Forgot password?
              </Link>
            </div>

            <button className="bg-[#263339] mx-auto w-36 h-14 rounded-2xl shadow-sm hover:shadow-lg">
              <Link to={"/home"}>Sign in</Link>
            </button>

            {/* <button className="bg-[#263339] mx-auto w-36 h-14 rounded-2xl shadow-sm hover:shadow-lg">
              Sign in
            </button> */}
          </form>
          <p className="text-slate-200 text-center mt-1">
            Don’t have an account?{" "}
            <span className="text-[#0066A4] pl-2 text-sm">
              <Link to={"/signup"} className="">
                Sign-up
              </Link>
            </span>
          </p>
        </div>
        <div className="">
          <img src={amico} className="w-[590px] " />
        </div>
      </div>
    </div>
  );
};

export default Login;
