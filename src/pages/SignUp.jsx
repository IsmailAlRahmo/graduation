import { useState } from "react";
import bro from "../assets/images/bro.svg";
import { useMutation } from "react-query";

const login = async (data) => {
  // const response = await fetch("http://iptv.likesyria.sy/new_bill/auth", {
  //   method: "POST",
  //   headers: {
  //     "Content-Type": "application/json",
  //   },
  //   body: JSON.stringify(data),
  // });
  const user = {
    username: "sam",
    id: 5,
  };
  if (!user) {
    throw new Error("Login failed");
  }

  return user;
};

const SignUp = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const mutation = useMutation(login, {
    onSuccess: (data) => {
      // Store user info in local storage
      localStorage.setItem("user", JSON.stringify(data));
      console.log("Login successful", data);
      // Update user state if needed, you can do this by setting a global state or using context
    },
    onError: (error) => {
      console.error("Login failed", error);
    },
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      console.error("Passwords do not match");
      return;
    }

    mutation.mutate({
      // username: username,
      email: email,
      password: password,
    });
  };
  return (
    <div className="w-full h-screen bg-gradient-to-br from-[#2C2C2C] to-[#012C61]">
      <div className=" w-full h-full flex flex-row justify-between items-center py-20 px-20">
        <div className="w-1/2 h-full flex flex-col pt-2 px-20 gap-6">
          <h1 className="text-2xl text-white text-center">Create an account</h1>
          <form
            onSubmit={handleSubmit}
            className="pt-10 flex flex-col gap-7 text-slate-200 w-full "
          >
            <input
              onChange={(e) => setUsername(e.target.value)}
              type="text"
              placeholder="Username"
              className=" h-14 bg-[#192535] pl-8 rounded-3xl focus:outline-none"
              value={username}
            />
            <input
              onChange={(e) => setEmail(e.target.value)}
              type="email"
              placeholder="E-mail Address"
              className=" h-14 bg-[#192535] pl-8 rounded-3xl focus:outline-none"
              value={email}
            />
            <input
              onChange={(e) => setPassword(e.target.value)}
              type="password"
              placeholder="Password"
              className=" h-14 bg-[#192535] pl-8 rounded-3xl focus:outline-none"
              value={password}
            />
            <input
              onChange={(e) => setConfirmPassword(e.target.value)}
              type="password"
              placeholder="Confirm Password"
              className=" h-14 bg-[#192535] pl-8 rounded-3xl focus:outline-none"
              value={confirmPassword}
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
