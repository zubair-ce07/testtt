import React from "react";
import Header from "./Header";

class Home extends React.Component{
    static isPrivate = true;
    render(){
    return (
        <div>
            <Header/>
            <h3>Welcome Home</h3>
        </div>
    );
    }
}

export default Home;
