import React, { Component } from 'react'
import './index.css';
import YTSearch from 'youtube-api-search'
import * as VideoComponent from './components/VideoComponents'

const API_KEY = 'AIzaSyB5wN5GvFkR7FSuiOaD5LC0svpx8WYlX4A';


function SearchBar(props) {
    return (
        <div>
            <input
                value={props.value}
                onChange={props.onChange}
            />

        </div>
    );
}


class App extends Component {
    constructor(props) {
        super(props);
        this.onInputChange = this.onInputChange.bind(this);
        this.state = {
            videos: [],
            selectedVideo: null,
            term: 'Search'
        };
    }

    onInputChange(event) {
        this.setState({term: event.target.value});
        YTSearch({key: API_KEY, term: this.state.term}, (videos) => this.setState({videos: videos}));
    }

    render() {
        return (
            <div>
                <div>
                    <SearchBar value={this.state.term} onChange={this.onInputChange}/>
                </div>
                <div>
                    <VideoComponent.VideoDetail video={ this.state.selectedVideo }/>
                </div>
                <div>
                    <VideoComponent.VideoList
                        videos={ this.state.videos }
                        onSelect={(selectedVideo) => this.setState({selectedVideo: selectedVideo})}
                    />
                </div>
            </div>
        );
    }
}

export default App;
