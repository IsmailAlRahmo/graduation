import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Home from "./pages/Home.jsx";
import Login from "./pages/Login.jsx";
import SignUp from "./pages/SignUp.jsx";
import ResetPassword from "./pages/ResetPassword.jsx";
import Overview from "./pages/Overview.jsx";
import App from "./App.jsx";
import MyVideos from "./pages/MyVideos.jsx";
import Reports from "./pages/Reports.jsx";
import StartRecording from "./pages/StartRecording.jsx";
import DummyWebSocket from "./pages/DummyWebSocket.jsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/dummy",
    element: <DummyWebSocket />,
  },
  {
    path: "signin",
    element: <Login />,
  },
  {
    path: "signup",
    element: <SignUp />,
  },
  {
    path: "reset-password",
    element: <ResetPassword />,
  },
  {
    path: "home",
    element: <App />,
    children: [
      {
        path: "/home/overview",
        element: <Overview />,
      },
      {
        path: "/home/videos",
        element: <MyVideos />,
      },
      {
        path: "/home/reports",
        element: <Reports />,
      },
      {
        path: "/home/record",
        element: <StartRecording />,
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
