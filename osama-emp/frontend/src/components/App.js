import React, { Component } from "react";
import "./App.css";
import Employee from "./Employee";
import djangoapi from "../djangoapi";

class App extends Component {
  constructor(props) {
    super();
    this.state = {
      results: []
    };
  }

  componentDidMount() {
    djangoapi.listEmployees(jsonData => {
      console.log(jsonData);
      this.setState({
        results: jsonData.results
      });
    });
  }

  render() {
    return (
      <div className="App">
        <ul>
          {this.state.results.map(current => {
            return <Employee emp={current} />;
          })}
        </ul>
      </div>
    );
  }
}

export default App;
