import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import { Provider } from "react-redux";
import "./index.css";
import AppContainer from "./components/AppContainer";
import registerServiceWorker from "./registerServiceWorker";
import Login from "./Login.js";
import { loggedIn } from "./auth";
import configureStore from "./configureStore";

let store = configureStore();

ReactDOM.render(
  <BrowserRouter history={BrowserRouter.browserHistory}>
    {loggedIn()
      ? <Provider store={store}>
          <AppContainer />
        </Provider>
      : <Login />}
  </BrowserRouter>,
  document.getElementById("root")
);
registerServiceWorker();
