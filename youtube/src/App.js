import React, { Component } from 'react';
import './App.css';
import SearchBar from './components/searchbar';
import Result from './components/result';
import YTSearch from 'youtube-api-search';

const youtube_key = 'AIzaSyCBjMkA8HpsfJ72n3DiLhWLOGWIZKUE1IA';

class App extends Component {
  constructor(props)
  {
    super(props);
    this.state = {result_videos: []}
    this.searchYouTube('react tutorial')
  }

  searchYouTube(search_term)
  {
    YTSearch({key: youtube_key, term: search_term, limit: 5}, (videos) => {this.setState({result_videos: videos})})
  }

  render() {
    return (
      <div>
            <nav className="navbar navbar-dark bg-dark" >
                <a href="homepage.jsx"> <div className="navbar-brand">YouTube</div> </a>
                <SearchBar className="navbar-brand" onSearch={(search_term) => this.searchYouTube(search_term)}/>
            </nav>
            <div className="mt-3">
                <Result videos={this.state.result_videos}/>
            </div>
      </div>
    );
  }
}

export default App;
