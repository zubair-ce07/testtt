import React, { Component } from 'react';
import {urlFormer, fetchData} from '../utils.js';
import Search from './search.js'
import Player from './player.js'
import VideoList from './videoList.js'


class Youtube extends Component {
  constructor(props) {
    super(props)
    this.state = {
      listSources: Array(5).fill(null),
      playerSource : null
    }
  }

  updateList(url)
  {
    fetchData(url)
      .then((result) => {
        let listSources = []
        for (let item of result.items)
        {
          let videoIcon = {
            'title': item.snippet.title,
            'description': item.snippet.description,
            'thumbnail': item.snippet.thumbnails.default.url,
            'id': item.id.videoId
          }
          listSources.push(videoIcon)
        }
        this.setState({listSources})
      })
      .catch(console.error);
  }

  search(query) {
    let url = urlFormer(query, null)
    this.updateList(url)
  }

  onSelect(icon)
  {
    this.setState({playerSource: icon});
    let url =  urlFormer(null, icon.id)
    this.updateList(url)
  }

  render() {
    return (
      <div className="youtube">
        <Search onClick={this.search.bind(this)} />
        <Player source={this.state.playerSource} />
        <VideoList
          sources={this.state.listSources}
          onSelect={this.onSelect.bind(this)}
        />
      </div>
    )
  }
}


export default Youtube;
