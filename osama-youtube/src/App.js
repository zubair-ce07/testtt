import React, { Component } from "react";
import "./App.css";
import SearchForm from "./SearchForm.js";
import Result from "./Result.js";
import ResultList from "./ResultList.js";
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
      vidId: vidId
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

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <SearchForm searchHandler={this.searchYoutube} />
        </div>

        {(function(playVid, vidId) {
          if (playVid) {
            return <VideoPlayer play={playVid} vidId={vidId} />;
          }
        })(this.state.playVid, this.state.vidId)}

        <div className="result-container">
          {/* <ResultList list={this.state.results} /> */}
          {(function(state, playFunction) {
            return state.results.map(item => {
              return (
                <Result
                  key={item.etag}
                  imgurl={item.snippet.thumbnails.medium.url}
                  title={item.snippet.title}
                  description={item.snippet.description}
                  vidId={item.id.videoId}
                  play={playFunction}
                />
              );
            });
          })(this.state, this.playVideo)}
        </div>
      </div>
    );
  }
}

export default App;
