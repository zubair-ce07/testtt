import React, { Component } from "react";

import "./App.css";
import SearchForm from "../containers/SearchForm";
import ResultContainer from "../containers/ResultContainer";
import VideoContainer from "../containers/VideoContainer";
class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <SearchForm />
        </div>
        <VideoContainer />
        <ResultContainer />
      </div>
    );
  }
}

export default App;
