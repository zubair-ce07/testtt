import React from "react";
import AuthenticatedHome from "./AuthenticatedHome";
import Header from "./Header";

class Home extends React.Component{
    static isPrivate = true;
    render(){
    return (
        <div>
            <Header/>
            <AuthenticatedHome/>
        </div>
    );
    }
}

export default Home;
