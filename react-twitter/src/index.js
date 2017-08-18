import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import {BrowserRouter as Router, Route} from "react-router-dom";
import Home from "./components/Home";
import Logout from "./components/Logout";


class App extends React.Component {
    render() {
        return (
            <Router>
                <div>
                    <Route exact path="/" component={Home}/>
                    <Route exact path="/logout" component={Logout}/>
                </div>
            </Router>
        );
    }
}

ReactDOM.render(
    <App/>,
    document.getElementById('root')
);
