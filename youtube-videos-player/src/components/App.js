import React, { Component } from 'react';
import { Route } from 'react-router-dom';
import * as YoutubeAPI from '../utils/YoutubeAPI'
import { DEFAULT_SEARCH_QUERY, ROUTE_PREFIX } from '../configs/'
import Home from './home/';
import '../App.css';

class App extends Component {
  // App component

  state = {
    videos: [],
    mainVideo: {}
  };

  componentDidMount() {
    this.searchOnYoutube(DEFAULT_SEARCH_QUERY);
  }

  searchOnYoutube = (searchQuery) => {
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
    this.setState({
      mainVideo: video
    });
  };


  render() {
    const { videos, mainVideo } = this.state;

    return (
      <Route exact path={ROUTE_PREFIX} render={() => (
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
