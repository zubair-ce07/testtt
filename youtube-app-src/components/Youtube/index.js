import React, { Component } from 'react';
import { urlFormer } from '../../shared/utils.js';
import { fetchData } from '../../shared/apiCaller.js';
import Search from '../Search';
import Player from '../Player';
import VideoList from '../VideoList';

class Youtube extends Component {
  state = {
    listSources: null,
    playerSource: null
  };

  updateList = data => {
    debugger;
    let listSources = [];
    for (let item of data.items) {
      let videoIcon = {
        title: item.snippet.title,
        description: item.snippet.description,
        thumbnail: item.snippet.thumbnails.default.url,
        id: item.id.videoId
      };
      listSources.push(videoIcon);
    }
    this.setState({ listSources });
  };

  search = () => {
    let query = document.getElementById('searchInput').value;
    let url = urlFormer(query, null);
    fetchData(url, this.updateList);
  };

  onSelect = icon => {
    this.setState({ playerSource: icon });
    let url = urlFormer(null, icon.id);
    fetchData(url, this.updateList);
  };

  render() {
    return (
      <div className="youtube">
        <Search onClick={this.search} />
        <Player source={this.state.playerSource} />
        <VideoList sources={this.state.listSources} onSelect={this.onSelect} />
      </div>
    );
  }
}

export default Youtube;
