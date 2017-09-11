import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import AuthRoute from "./components/AuthRoute";
import Home from "./components/Home";
import LoginForm from "./components/LoginForm";
import News from "./components/News";
import NewsDetailed from "./components/NewsDetailed";
import Header from "./components/Header";


class App extends React.Component {
    render() {
        return (
            <Router>
                <div>
                    <Route component={Header}/>
                    <Switch>
                        <AuthRoute exact path="/" component={Home}/>
                        <AuthRoute path="/login" component={LoginForm}/>
                        <AuthRoute exact path="/news" component={News}/>
                        <AuthRoute path={"/news/:id"} component={NewsDetailed}/>
                    </Switch>
                </div>

            </Router>
        );
    }
}

ReactDOM.render(
    <App/>,
    document.getElementById('root')
);
