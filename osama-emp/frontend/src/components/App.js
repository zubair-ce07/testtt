import React, { Component } from "react";
import "./App.css";
import Employee from "./Employee";
import djangoapi from "../djangoapi";

class App extends Component {
  constructor(props) {
    super();
    this.state = {
      username: "",
      profile: {},
      results: []
    };
  }

  componentDidMount() {
    djangoapi.getProfile(jsonData => {
      console.log(jsonData);
      this.setState({
        profile: jsonData
      });
    });
  }

  render() {
    return (
      <div className="App">
        <ul>
          <li>
             {this.state.profile.username} 
          </li>
        </ul>
      </div>
    );
  }
}

export default App;
