import React from "react";
import { Provider } from "react-redux";
import ReactDOM from "react-dom";
import LoginView from "./containers/login";
import {SignUpView} from "./containers/signup/signupView";
import { store } from "./app/configureStore";

ReactDOM.render(
  <Provider store={store}>
    <LoginView />
  </Provider>,
  document.querySelector("#root")
);