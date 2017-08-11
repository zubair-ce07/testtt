import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import configureStore from "./configureStore";
import "./index.css";
import App from "./components/App";
import { startSearchRequest } from "./actions";
import registerServiceWorker from "./registerServiceWorker";

const store = configureStore();

store.dispatch(startSearchRequest(""));

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById("root")
);
registerServiceWorker();
