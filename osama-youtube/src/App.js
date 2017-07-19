import React, { Component } from "react";
import "./App.css";
import SearchForm from "./SearchForm.js";
import Result from "./Result.js";
import VideoPlayer from "./VideoPlayer.js";
import * as youtube from "./fetch.js";

class App extends Component {
  constructor() {
    super();
    this.searchYoutube = this.searchYoutube.bind(this);
    this.playVideo = this.playVideo.bind(this);
    this.state = {
      playVid: false,
      vidId: "",
      results: []
    };
  }

  playVideo(vidId) {
    this.setState({
      playVid: true,
      vidId
    });
  }

  searchYoutube(query) {
    youtube.search(jsonData => {
      this.setState({
        results: jsonData.items
      });
    }, query);
  }

  componentDidMount() {
    this.searchYoutube("");
  }

  scrolled(evt) {
    console.log(evt.target.getBoundingClientRect());
  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <SearchForm searchHandler={this.searchYoutube} />
        </div>
        {this.state.playVid &&
          <div className="player-container">
            <VideoPlayer vidId={this.state.vidId} />
          </div>}

        <div className="result-container">
          {this.state.results.map(item =>
            <Result
              key={item.etag}
              imgurl={item.snippet.thumbnails.medium.url}
              title={item.snippet.title}
              description={item.snippet.description}
              vidId={item.id.videoId}
              play={this.playVideo}
            />
          )}
        </div>
      </div>
    );
  }
}

export default App;
