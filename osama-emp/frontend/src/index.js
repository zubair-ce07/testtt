import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Route, browserHistory } from "react-router-dom";
import "./index.css";
import App from "./components/App";
import registerServiceWorker from "./registerServiceWorker";
var Login = require("./login");
var auth = require("./auth");

function requireAuth(nextState, replace) {
  if (!auth.loggedIn()) {
    replace({
      pathname: "/api-auth/login/",
      state: { nextPathname: "/employees/" }
    });
  }
}

ReactDOM.render(
  <BrowserRouter history={BrowserRouter.browserHistory}>
    <Route path="/api-auth/login/" component={Login} />
    {/* <Route path="/employees/" component={App} onEnter={requireAuth} /> */}
  </BrowserRouter>,
  document.getElementById("root")
);
registerServiceWorker();
