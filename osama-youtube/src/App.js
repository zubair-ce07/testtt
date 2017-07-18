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
      vidId: false,
      results: []
    };
  }

  playVideo(vidId) {
    this.setState({
      vidId: vidId
    });
  }

  searchYoutube(query) {
    var that = this;
    youtube.search(jsonData => {
      that.setState({
        results: jsonData.items.map((item, key) => {
          return (
            <Result
              key={item.etag}
              imgurl={item.snippet.thumbnails.medium.url}
              title={item.snippet.title}
              description={item.snippet.description}
              vidId={item.id.videoId}
              play={this.playVideo}
            />
          );
        })
      });
    }, query);
  }

  componentDidMount() {
    this.searchYoutube("");
  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <SearchForm searchHandler={this.searchYoutube} />
        </div>
        <VideoPlayer vid={this.state.vidId} />
        <div className="result-container">
          {this.state.results}
        </div>
      </div>
    );
  }
}

export default App;
