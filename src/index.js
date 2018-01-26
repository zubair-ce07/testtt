import React from "react";
import ReactDOM from "react-dom";
import UI from "./App";
import {Router, Route} from "react-router";
import createBrowserHistory from "history/createBrowserHistory";
import SignUp from "./signup";
import Login from "./login";
const newHistory = createBrowserHistory();

class Root extends React.Component{
    render(){
        return(
            <Router history={newHistory}>
                <div>
                    <Route exact path="/" component={UI} />
                    <Route path="/login" component={Login} />
                    <Route path="/signup" component={SignUp} />
                </div>
            </Router>
        )
    }
}

ReactDOM.render(<Root />, document.getElementById('root'));

