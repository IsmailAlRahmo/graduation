import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import {
  createBrowserRouter,
  Navigate,
  RouterProvider,
} from "react-router-dom";
import Home from "./pages/Home.jsx";
import Login from "./pages/Login.jsx";
import SignUp from "./pages/SignUp.jsx";
import ResetPassword from "./pages/ResetPassword.jsx";
import Overview from "./pages/Overview.jsx";
import App from "./App.jsx";
import MyVideos from "./pages/MyVideos.jsx";
import Reports from "./pages/Reports.jsx";
// import DummyWebSocket from "./pages/DummyWebSocket.jsx";
import { QueryClient, QueryClientProvider } from "react-query";
import { useUser } from "./auth/useUser.jsx";
import Live from "./pages/Live.jsx";
import DummyWebSocket from "./pages/DummyWebSocket.jsx";
import VideoDetail from "./pages/VideoDetail.jsx";

function ProtectedRoute({ children }) {
  const { user } = useUser();
  // if (!user) return <Navigate to="/signin" replace />;

  return <>{children}</>;
}
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
    path: "/home/record",
    element: <Live />,
  },
  {
    path: "/home",
    element: (
      <ProtectedRoute>
        <App />
      </ProtectedRoute>
    ),
    children: [
      {
        path: "overview",
        element: <Overview />,
      },
      {
        path: "videos",
        element: <MyVideos />,
      },
      {
        path: "reports",
        element: <Reports />,
      },
      {
        path: "videos/:id", // Route for video details
        element: <VideoDetail />,
      },
    ],
  },
]);
const queryClient = new QueryClient();
ReactDOM.createRoot(document.getElementById("root")).render(
  <div>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </div>
);
