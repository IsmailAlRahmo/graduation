

const ResetPassword = () => {
  return (
    <div className="w-full h-screen bg-gradient-to-br from-[#2C2C2C] to-[#012C61] flex flex-col items-center justify-center">
      <form className="flex flex-col gap-8 w-2/5 h-4/5 justify-start items-center pt-10 text-slate-200">
        <h1 className="text-3xl mb-10">Reset your password</h1>
        <input
          type="text"
          placeholder="E-mail Address"
          className=" h-12 bg-[#192535] pl-8 rounded-3xl focus:outline-none w-full"
        />
        <input
          type="password"
          placeholder="Password"
          className=" h-12 bg-[#192535] pl-8 rounded-3xl focus:outline-none w-full"
        />
        <input
          type="password"
          placeholder="Confirm Password"
          className=" h-12 bg-[#192535] pl-8 rounded-3xl focus:outline-none w-full"
        />
        <button className="rounded-3xl w-44 h-12 text-[#263339] flex items-center justify-center border-[#263339] border-2 bg-white mt-6">
          Reset
        </button>
      </form>
    </div>
  );
};

export default ResetPassword;
