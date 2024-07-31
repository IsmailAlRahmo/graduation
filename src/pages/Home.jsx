
import rafiki from "../assets/images/rafiki.svg";
const Home = () => {
  return (
    <div className="w-full h-screen bg-gradient-to-br from-[#F5F5F5] to-[#012C61]">
      <div className="flex justify-center items-center px-40 py-28 ">
        <section className="w-2/3 flex flex-col gap-6">
          <h1 className="w-[503px] text-6xl text-[#263339] leading-[70px] font-bold drop-shadow-xl">
            Improve Your Skills
          </h1>
          <div className=" w-[234px] border-2 border-[#263339]"></div>
          <p>
            It’s your destination to improve your public speaking skills. Enjoy
            the experience of giving your presentation and get a feedback on
            your performance about your body language, facial expressions and
            vocal tone. harry up and join us now!{" "}
          </p>
          <div className="flex justify-around items-center p-4">
            <a
              href="signup"
              className="bg-[#263339] rounded-3xl w-44 h-12 text-slate-100 flex items-center justify-center"
            >
              <p className="font-semibold">Sign-up</p>
            </a>
            <a
              href="login"
              className="rounded-3xl w-44 h-12 text-[#263339] flex items-center justify-center border-[#263339] border-2 bg-white"
            >
              <p className="font-semibold">Login</p>
            </a>
            <a></a>
          </div>
        </section>
        <section>
          <img src={rafiki} className="" />
        </section>
      </div>
    </div>
  );
};

export default Home;
