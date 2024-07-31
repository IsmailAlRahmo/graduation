
import Home from "./pages/Home";
import SignUp from "./pages/SignUp";
import Login from "./pages/Login";
import ResetPassword from "./pages/ResetPassword";


function App() {
  return (
    <div className="w-full h-screen ">
      <Home />
      <SignUp/>
      <Login/>
      <ResetPassword/>
    </div>
  );
}

export default App;
