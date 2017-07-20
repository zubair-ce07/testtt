import React, { Component } from "react";
import { Route, Link } from "react-router-dom";
import "./App.css";
import SearchForm from "./SearchForm.js";
import Result from "./Result.js";
import VideoPlayer from "./VideoPlayer.js";

import * as youtube from "./youtubeapi.js";

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

  render() {
    return (
      <div className="App">
        <Route
          path="/"
          render={() =>
            <div className="App-header">
              <SearchForm searchHandler={this.searchYoutube} />
            </div>}
        />

        <Route
          path="/video"
          render={() =>
            this.state.playVid &&
            <div className="player-container">
              <VideoPlayer vidId={this.state.vidId} />
              <Link to="/search" className="backlink">Back</Link>
            </div>}
        />

        <Route
          path="/search"
          render={() =>
            <div className="result-container">
              {this.state.results.length !== 0
                ? this.state.results.map(item =>
                    <Link to="/video">
                      <Result
                        key={item.etag}
                        imgurl={item.snippet.thumbnails.medium.url}
                        title={item.snippet.title}
                        description={item.snippet.description}
                        vidId={item.id.videoId}
                        play={this.playVideo}
                      />
                    </Link>
                  )
                : <h1>Sorry, There are no results to display</h1>}
            </div>}
        />
      </div>
    );
  }
}

export default App;
