import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import {BrowserRouter as Router, Switch} from "react-router-dom";
import Route from "./components/AuthRoute";
import Home from "./components/Home";
import LoginForm from "./components/LoginForm";
import News from "./components/News";


class App extends React.Component {
    render() {
        return (
            <Router>
                <Switch>
                    <Route exact path="/" component={Home}/>
                    <Route path="/login" component={LoginForm}/>
                    <Route path="/news" component={News}/>
                </Switch>
            </Router>
        );
    }
}

ReactDOM.render(
    <App/>,
    document.getElementById('root')
);








