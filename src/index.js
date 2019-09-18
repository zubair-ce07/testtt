import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import * as serviceWorker from "./serviceWorker";
import App from './App'

class AppRoot extends React.Component {
    render() {
        return(
            <App />
        );
    }
}


ReactDOM.render(<AppRoot />, document.getElementById("root"));
serviceWorker.register();
