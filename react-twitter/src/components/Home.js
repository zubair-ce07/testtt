import React from "react";
import LoginForm from "./LoginForm";
import AuthenticatedHome from "./AuthenticatedHome";
import Header from "./Header";

function Main(props) {
    if (localStorage.user)
        return <AuthenticatedHome/>;
    return <LoginForm/>;
}


function Home(props) {
    return (
        <div>
            <Header/>
            <Main/>
        </div>
    );
}

export default Home;