import React, { Component } from 'react';
import Url from "domurl";
import axios from 'axios'

import SearchBar from './SearchBar.js';
import VideoList from './VideoList.js';
import './App.css';


class App extends Component {

  constructor() {
    super();
    this.state = {
      videoList: [],
    }
  }

  changeSearchText = searchText => {
    var searchUrl = new Url("https://www.googleapis.com/youtube/v3/search?&key=AIzaSyBcI8VM_RAoY6jJHzktFqEZbzLedg2_oKc");
    searchUrl.query.q = searchText;
    searchUrl.query.part = "snippet";
    searchUrl.query.maxResults = 20;

    axios.get(searchUrl).then(Response => {
      this.setState({
        videoList: Response.data.items
      })

    });
  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <SearchBar
            onUserInput={this.changeSearchText}
          />
        </div>
        <p className="App-intro">
          {this.state.videoList.length > 0 &&
            <VideoList
              videos={this.state.videoList}
            />
          }
        </p>
      </div>
    );
  }
}

export default App;
