import React from "react";
import Home from "./Home";
import withRouter from "react-router-dom/es/withRouter";

function Logout(props) {
    localStorage.clear();
    props.history.push('/')
    return (
        <Home/>
    )
}

export default withRouter(Logout);