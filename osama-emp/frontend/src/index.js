import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import { Provider } from "react-redux";
import "./index.css";
import App from "./components/App";
import registerServiceWorker from "./registerServiceWorker";
import Login from "./Login.js";
import { loggedIn } from "./auth";
import configureStore from "./configureStore";
import { getProfileStart } from "./actions";

let store = configureStore();

store.dispatch(getProfileStart(localStorage.username));

ReactDOM.render(
  <BrowserRouter history={BrowserRouter.browserHistory}>
    {loggedIn() ? <App /> : <Login />}
  </BrowserRouter>,
  document.getElementById("root")
);
registerServiceWorker();
