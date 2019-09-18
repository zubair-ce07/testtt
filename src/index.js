import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import * as serviceWorker from "./serviceWorker";
import {Container} from "@material-ui/core";
import AppSidebar from "./SharedComponents/AppSidebar/AppSidebar";
import Profile from "./UserComponents/Profile/profile";

class AppRoot extends React.Component {
    render() {
        return (
            <div style={{backgroundColor: '#EBEBEB'}}>
                <AppSidebar />

                <Container style={{backgroundColor: '#EBEBEB'}}>
                    <Profile />
                </Container>

            </div>
        );
    }
}

ReactDOM.render(<AppRoot/>, document.getElementById("root"));
serviceWorker.register();
