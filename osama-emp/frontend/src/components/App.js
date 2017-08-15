import React, { Component } from "react";
import "./App.css";
import Employee from "./employee/Employee";
import Profile from "./profile/Profile";
import djangoapi from "../djangoapi";
import { loggedIn, logout } from "../auth.js";
import Login from "./Login";

class App extends Component {
  constructor(props) {
    super();
    this.state = {
      userProfile: {},
      displayProfile: {},
      token: null
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

  login = (username, password) => {
    djangoapi.login(username, password, jsonData => {
      this.setState({
        token: jsonData.token
      });
    });
  };

  logout = () => {
    this.setState({
      token: null
    });
  };

  render() {
    return this.token
      ? <Login />
      : <div className="App">
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
        </div>;
  }
}

export default App;
