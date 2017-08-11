import React, { Component } from "react";
import { connect } from "react-redux";
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
        {this.props.playVid && <VideoContainer />}
        {this.props.results.length > 0 && <ResultContainer />}
      </div>
    );
  }
}

function mapStateToProps(state) {
  return {
    playVid: state.playVid,
    results: state.results
  };
}

export default connect(mapStateToProps, null)(App);
