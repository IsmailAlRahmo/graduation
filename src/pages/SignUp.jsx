
import bro from "../assets/images/bro.svg";
const SignUp = () => {
  return (
    <div className="w-full h-screen bg-gradient-to-br from-[#2C2C2C] to-[#012C61]">
      <div className=" w-full h-full flex flex-row justify-between items-center py-20 px-20">
        <div className="w-1/2 h-full flex flex-col pt-2 px-20 gap-6">
          <h1 className="text-2xl text-white text-center">Create an account</h1>
          <form className="pt-10 flex flex-col gap-7 text-slate-200 w-full ">
            <input
              type="text"
              placeholder="Username"
              className=" h-14 bg-[#192535] pl-8 rounded-3xl focus:outline-none"
            />
            <input
              type="text"
              placeholder="E-mail Address"
              className=" h-14 bg-[#192535] pl-8 rounded-3xl focus:outline-none"
            />
            <input
              type="password"
              placeholder="Password"
              className=" h-14 bg-[#192535] pl-8 rounded-3xl focus:outline-none"
            />
            <input
              type="password"
              placeholder="Confirm Password"
              className=" h-14 bg-[#192535] pl-8 rounded-3xl focus:outline-none"
            />
            <button className="bg-[#263339] mx-auto w-36 h-14 rounded-2xl shadow-sm hover:shadow-lg">
              Sign-up
            </button>
          </form>
        </div>
        <div className="">
          <img src={bro} className="mb-10" />
        </div>
      </div>
    </div>
  );
};

export default SignUp;
