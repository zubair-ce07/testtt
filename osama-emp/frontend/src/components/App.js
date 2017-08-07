import React, { Component } from "react";
import { Route } from "react-router-dom";
import "./App.css";
import Employee from "./employee/Employee";
import HierarchyContainer from "./hierarchy/HierarchyContainer";
import { loggedIn } from "../auth.js";

class App extends Component {
  componentDidMount() {
    
  }

  render() {
    return (
      <div className="App">
        {/* {loggedIn() && <Employee emp={this.props.profile} />}  */}
        <br />
        <HierarchyContainer />
      </div>
    );
  }
}

export default App;
