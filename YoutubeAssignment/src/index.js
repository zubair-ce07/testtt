import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import YTSearch from 'youtube-api-search';

import SearchBar from './components/search_bar'
import VideosList from './components/recommented_list'
import VideoDetail from './components/video_details'

const key = 'AIzaSyDGKv38Ed7PF9lG6CUpHLSj965SBEnvf_4';

class App extends Component{

    constructor(prop) {
        super(prop);
        this.state = {
            videosList: [],
            selectedVideo: null
        };
        this.searchVideos("coke studio");
    }//constructor

    render(){

        return (
            <div>
                <SearchBar onQueryChange={ queryText => this.searchVideos(queryText)}/>

                <VideoDetail videoItem={this.state.selectedVideo} />

                <VideosList
                    onVideoSelection={selectedVideo => this.setState({selectedVideo})}
                    videosList={this.state.videosList}
                />
            </div>
        );
    }//render

    searchVideos(queryText){
        YTSearch({key: key, term: queryText}, videosList => {
            this.setState({
                videosList: videosList,
                selectedVideo: videosList[0]
            });
        });
    }//searchVideos

}//class

ReactDOM.render(<App />, document.querySelector('.container'));
