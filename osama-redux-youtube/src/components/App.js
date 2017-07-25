import React, { Component } from "react";

import "./App.css";
import SearchForm from "../containers/SearchForm";
import ResultContainer from "../containers/ResultContainer";

class App extends Component {
  constructor(props) {
    super();
    this.playVideo = this.playVideo.bind(this);
  }

  playVideo(vidId) {
    this.setState({
      playVid: true,
      vidId
    });
  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <SearchForm />
        </div>
        {/* {this.state.playVid &&
          <div className="player-container">
            <VideoPlayer vidId={this.state.vidId} />
          </div>} */}
        <div className="result-container">
          <ResultContainer />
        </div>
      </div>
    );
  }
}

export default App;
