import React from "react";
import { Provider } from "react-redux";
import ReactDOM from "react-dom";
import { PersistGate } from 'redux-persist/integration/react'
import { store, persistor } from "./app/configureStore";
import { AppContainer } from "./containers";

ReactDOM.render(
  <Provider store={store}>
    <PersistGate loading={null} persistor={persistor}>
    <AppContainer />
    </PersistGate>
  </Provider>,
  document.querySelector("#root")
);
