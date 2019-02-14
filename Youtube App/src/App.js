import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import SearchBar from './components/search_bar';
import YoutubeAPISearch from 'youtube-api-search';
import VideoList from './components/video_list'; 
import VideoDetail from './components/video_detail';
const API_KEY = 'AIzaSyDGuP6-UPfIq4XcRIA7-WYe6lNAtJjeFAA';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = { 
      videos: [],
      selectedVideo: null
    };

    this.videoSearch('')
  }

  videoSearch(term) {
    YoutubeAPISearch({key: API_KEY, term: term}, (data) => {
      this.setState({
        videos: data,
        selectedVideo: null
      });
    });
  }

  videoSelect(selectedVideo) {
    this.setState({
      selectedVideo: selectedVideo
    });
  }

  render() {
    return (
      <div>
        
        <div className="row">
          <div className="col-lg-5"></div>
          <div className="col-lg-7"><h4 className="page-heading">Youtube Search App</h4></div> 
        </div>
        <div className="row">
          <div className="col-lg-3"></div>
          <div className="col-lg-9">
            <SearchBar onSearchTermChange={searchTerm => this.videoSearch(searchTerm)} />
          </div>
        </div>
        <div className="row video-panel">
          <div className="col-lg-1"></div>
          <div className={this.state.selectedVideo ? "col-lg-7" : ""}>
            <VideoDetail video={this.state.selectedVideo} />
          </div>
          <div className="col-lg-4">
            <div className={this.state.selectedVideo ? "related-videos" : ""}>
              <VideoList onVideoSelect={selectedVideo => this.videoSelect(selectedVideo)}
                videos={this.state.videos} />
            </div>
          </div>
        </div>

      </div>
    );
  }
}

export default App;
