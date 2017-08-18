import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import {BrowserRouter as Router} from "react-router-dom";
import Route from "./components/AuthRoute";
import Home from "./components/Home";
import LoginForm from "./components/LoginForm";


class App extends React.Component {
    render() {
        return (
            <Router>
                <div>
                    <Route path="/" component={Home}/>
                    <Route path="/login" component={LoginForm}/>
                </div>
            </Router>
        );
    }
}

ReactDOM.render(
    <App/>,
    document.getElementById('root')
);








