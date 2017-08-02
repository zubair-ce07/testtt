import React, { Component } from "react";
import "./App.css";
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
            return (
              <li key={current.username}>
                <p>
                  {current.username}
                </p>
                <p>
                  {current.reports_to}
                </p>
                <p>
                  {current.directs}
                </p>
              </li>
            );
          })}
        </ul>
      </div>
    );
  }
}

export default App;
