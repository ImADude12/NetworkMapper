import React from "react";
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
  // {
  //   path: "/login",
  //   element: <Login />,
  // },
];
