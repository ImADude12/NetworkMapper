import React from "react";
import { Configuration } from "./Pages/Configuration";
import { Home } from "./Pages/Home";
import Login from "./Pages/Login";

export const routes = [
  {
    path: "/",
    element: <Login />,
  },
  {
    path: "/home",
    element: <Home />,
  },
  {
    path: "/config",
    element: <Configuration />,
  },
];
