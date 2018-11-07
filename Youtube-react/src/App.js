import React, { Component } from 'react';
import axios from 'axios';
import {SearchBar} from './SearchBar.js';
import {Cards} from './Cards.js';
import {VideoPlayer} from './VideoPlayer.js';
import './App.css';

const apiUrl='https://www.googleapis.com/youtube/v3/'
const key='AIzaSyCv3KW6DhugN2yfS5HfN97tOt4525SDyio'
const maxResults=10
const type='video'
const part='snippet'


const marginTop={
  'marginTop': 30,
}

class App extends Component {
  state = {'query':'',
   'items': [],
   'nextPageToken': '',
   'videoId':'',
  }

  getData=(items=[], nextPageToken='')=>{
    let {query}= this.state;
    let url=`${apiUrl}search?maxResults=${maxResults}&part=${part}&order=viewCount&q=${query}&type=${type}&videoDefinition=high&key=${key}`
    if (nextPageToken !== ''){
      url =`${url}&pageToken=${nextPageToken}`
    }
    axios.get(url)
      .then(response =>{
          this.setState({ 'nextPageToken': response.data.nextPageToken, 'items': items.concat(response.data.items),});
  });
  }

    onChangeHandler = (value)=>{
        this.setState({'query': value});
    }
    searchClick = ()=>{
        this.getData();
    }

    loadMoreClick = ()=>{
      let {items, nextPageToken}= this.state;
      this.getData(items, nextPageToken);
    }
    
    videoCardClick=(videoId)=>{
      this.setState({'videoId': videoId})
    }


  render() {
    const {videoId, query, items, nextPageToken}=this.state
    return (
      <div className="App">
        <header  className="App-header"> 
        <div style={marginTop}>
            <SearchBar query={query} searchClick={this.searchClick} onChange={this.onChangeHandler} />
            {
              videoId ?<VideoPlayer  videoId={videoId} />: null
            }
          <Cards onClickHandler={this.videoCardClick} dataJson={items} />
        </div>
        {
          nextPageToken?<button onClick={this.loadMoreClick}>Load More</button>:null
        }
        </header>
      </div>
    );
  }
}

export default App;
