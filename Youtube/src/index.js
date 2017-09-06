import React, { Component } from 'react'
import ReactDom from 'react-dom'
import YTSearch from 'youtube-api-search'
import SearchBar from './components/search_bar'
import VideoList from './components/video_list'
import VideoDetail from './components/video_detail'

const API_KEY = 'AIzaSyApyyQv5cfQePPGDzBl5oyOsSFIYxLG3mA'


class App extends Component {
    constructor(props) {
        super(props);

        this.state = { 
            videos: [],
            selectedVideo: null
         };

        YTSearch({key:API_KEY, term: 'surfboards'}, 
            (videos) => {
                this.setState({ 
                    videos,
                    selectedVideo: videos[0]
                 });
                //same as this.setState({ videos:videos })
            }
        );
    }

    render() {
        return (
            <div>
                <SearchBar />
                <VideoDetail video={ this.state.selectedVideo }/>
                <VideoList
                    onVideoSelect={selectedVideo => this.setState({selectedVideo})} 
                    videos={ this.state.videos } />

            </div>
        );
    }
}


ReactDom.render(<App />, document.querySelector('.container'));