import React from "react";
import * as serviceWorker from "./serviceWorker";
import {Container} from "@material-ui/core";
import AppSidebar from "./SharedComponents/AppSidebar/AppSidebar";
import UserLoginRegistrationForm from "./UserComponents/LoginRegistrationForm/FormContainer/FormContainer";

class App extends React.Component {
  render() {
    return (
        <div style={{backgroundColor: '#EBEBEB'}}>
            <UserLoginRegistrationForm />
        </div>
    );
  }
}

export default App;