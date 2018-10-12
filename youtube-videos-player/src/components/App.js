import React, {Component} from 'react';
import {Route} from 'react-router-dom';
import * as YoutubeAPI from '../utils/YoutubeAPI'
import Home from './home/Home';
import '../App.css';

class App extends Component {
    // App component
    constructor(props) {
        super(props);

        this.state = {
            videos: [],
            mainVideo: {}
        };

        this.searchOnYoutube = this.searchOnYoutube.bind(this);
        this.playVideo = this.playVideo.bind(this);
    }

    componentDidMount() {
        // After components mount, call youtube videoes seach API
        this.searchOnYoutube('The new world order');
    }

    searchOnYoutube(searchQuery) {
        // Search on youtube videos search API and set state accordingly.
        YoutubeAPI.search(searchQuery, (videos) => {
            if (videos){
                this.setState({
                    videos: videos,
                    mainVideo: videos[0]
                });
            }
        })
    }

    playVideo(video){
        // Play video (set the video as main)
        this.setState({
            mainVideo: video
        });
    }


    render() {
        return (
            <Route exact path='/' render={() => (
                <Home
                    videos={this.state.videos}
                    mainVideo={this.state.mainVideo}
                    searchOnYoutube={this.searchOnYoutube}
                    playVideo={this.playVideo}
                />
            )}/>
        );
    }
}

export default App;
