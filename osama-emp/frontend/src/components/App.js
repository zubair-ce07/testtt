import React, { Component } from "react";
import { Route } from "react-router-dom";
import "./App.css";
import Employee from "./employee/Employee";
import Profile from "./profile/Profile";
import djangoapi from "../djangoapi";
import { loggedIn } from "../auth.js";

class App extends Component {
  constructor(props) {
    super();
    this.state = {
      userProfile: {},
      displayProfile: {}
    };
  }

  componentDidMount() {
    djangoapi.getProfile(localStorage.username, jsonData => {
      this.setState({
        userProfile: jsonData,
        displayProfile: jsonData
      });
    });
  }

  changeProfile = username => {
    djangoapi.getProfile(username, jsonData => {
      this.setState({
        displayProfile: jsonData
      });
    });
  };

  render() {
    return (
      <div className="App">
        <section>
          {loggedIn() &&
            <ul className="tree">
              <Employee
                emp={this.state.userProfile}
                profileHandler={this.changeProfile}
              />
            </ul>}
        </section>
        <section>
          <Profile profile={this.state.displayProfile} />
        </section>
      </div>
    );
  }
}

export default App;
