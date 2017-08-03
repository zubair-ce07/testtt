import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Redirect } from "react-router-dom";
import "./index.css";
import App from "./components/App";
import registerServiceWorker from "./registerServiceWorker";
import Login from "./Login.js";
import { loggedIn } from "./auth";

ReactDOM.render(
  <BrowserRouter history={BrowserRouter.browserHistory}>
    {loggedIn()
      ? <div>
          <Redirect to="/employees/" />
          <App />
        </div>
      : <Login />}
  </BrowserRouter>,
  document.getElementById("root")
);
registerServiceWorker();
