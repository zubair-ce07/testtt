import React, { Component } from "react";
import "./App.css";

class App extends Component {
  constructor(props) {
    super();
    this.state = {
      results: []
    };
  }

  api_call() {
    let that = this;
    fetch("http://localhost:8000/employees/", {
      method: "get"
    })
      .then(function(response) {
        return response.json();
      })
      .then(function(jsonData) {
        that.setState({
          results: jsonData.results
        });
      });
  }

  componentDidMount() {
    this.api_call();
  }

  render() {
    return (
      <div className="App">
        <ul>
          {this.state.results.map(current => {
            return (
              <li key={current.username}>
                {current.username}
              </li>
            );
          })}
        </ul>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
      </div>
    );
  }
}

export default App;
