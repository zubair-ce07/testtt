import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./components/App";
import registerServiceWorker from "./registerServiceWorker";
import Login from "./Login.js";
import { loggedIn } from "./auth";

ReactDOM.render(
  <div>
    {loggedIn() ? <App /> : <Login />}
  </div>,
  document.getElementById("root")
);
registerServiceWorker();
