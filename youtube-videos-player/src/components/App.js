import React, { Component } from 'react';
import { Route } from 'react-router-dom';
import * as YoutubeAPI from '../utils/YoutubeAPI'
import { StartSearchQuery } from '../configs/'
import Home from './home/';
import '../App.css';

class App extends Component {
  // App component

  state = {
    videos: [],
    mainVideo: {}
  };

  componentDidMount() {
    this.searchOnYoutube(StartSearchQuery);
  }

  searchOnYoutube = (searchQuery) => {
    // Search on youtube videos search API and set state accordingly.
    YoutubeAPI.search(searchQuery, (videos) => {
      if (videos) {
        this.setState({
          videos: videos,
          mainVideo: videos[0]
        });
      }
    })
  };

  playVideo = (video) => {
    // Play video (set the video as main)
    this.setState({
      mainVideo: video
    });
  };


  render() {
    const {videos, mainVideo} = this.state;

    return (
      <Route exact path='/' render={() => (
        <Home
          videos={videos}
          mainVideo={mainVideo}
          searchOnYoutube={this.searchOnYoutube}
          playVideo={this.playVideo}
        />
      )}/>
    );
  }
}

export default App;
