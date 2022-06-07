import { routes } from "./routes";
import { Routes, Route } from "react-router-dom";
import { theme } from "./global-styles/theme";
import { ThemeProvider } from "styled-components";
import { GlobalStyles } from "./global-styles/Global";
import React from "react";

const App = () => (
  <ThemeProvider theme={theme}>
    <GlobalStyles />
    <Routes>
      {routes.map(({ path, element }, idx) => (
        <Route path={path} element={element} key={idx} />
      ))}
    </Routes>
  </ThemeProvider>
);

export default App;

