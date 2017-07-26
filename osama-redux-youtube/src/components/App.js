import React, { Component } from "react";
import "./App.css";
import SearchForm from "./search/SearchFormContainer";
import ResultContainer from "./results/ResultContainer";
import VideoContainer from "./video/VideoPlayerContainer";

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
