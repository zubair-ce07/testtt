import React from 'react'
import './index.css';
import VideoList from './containers/VideoList'
import SearchBar from './containers/SearchBar'
import VideoDetail from './containers/VideoDetail'
import { connect } from 'react-redux'


class App extends React.Component {
    render() {
        return (
            <div>
                <div>
                    <SearchBar/>
                </div>
                {this.props.selectedVideo &&
                <div>
                    <VideoDetail/>
                </div>
                }
                <div>
                    <VideoList/>
                </div>
            </div>
        );
    }
}

function mapStateToProps(state){
    return {
        selectedVideo: state.selectedVideo
    };
}

App = connect(mapStateToProps)(App);

export default App
