import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import {applyMiddleware, createStore} from "redux";
import logger from "redux-logger";
import thunk from "redux-thunk";
import promise from "redux-promise-middleware";
import {Provider} from "react-redux";
import allReducers from "./reducers";
import App from "./components/App";
import registerServiceWorker from "./registerServiceWorker";

const middleware = applyMiddleware(promise(), thunk, logger);
const store = createStore(allReducers, middleware);
ReactDOM.render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById('root')
);
registerServiceWorker();
