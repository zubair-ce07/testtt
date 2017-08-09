import React, { Component } from "react";

import "./App.css";
import Employee from "./employee/Employee";
import Profile from "./profile/Profile";
import AppraisalModal from "./appraisal/AppraisalModal";

import djangoapi from "../djangoapi";
import { loggedIn, logout } from "../auth.js";

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
          <button
            id="logout"
            onClick={() => {
              logout();
              window.location.reload();
            }}
          >
            Log out
          </button>
        </section>
        <section>
          <Profile profile={this.state.displayProfile} />
        </section>
        <AppraisalModal />
      </div>
    );
  }
}

export default App;
