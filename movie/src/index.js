import React from "react";
import { Provider } from "react-redux";
import ReactDOM from "react-dom";
import { store } from "./app/configureStore";
import { AppContainer } from "./containers";

ReactDOM.render(
  <Provider store={store}>
    <AppContainer />
  </Provider>,
  document.querySelector("#root")
);
