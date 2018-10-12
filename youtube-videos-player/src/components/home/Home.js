import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Header from '../common/Header'
import VideoPlay from './VideoPlay'
import VideoGroup from './VideoGroup'

class Home extends Component {
    // Home component
    static propTypes = {
        videos: PropTypes.array.isRequired,
        mainVideo: PropTypes.object.isRequired,
        searchOnYoutube: PropTypes.func.isRequired,
        playVideo: PropTypes.func.isRequired,
    };


    render() {
        const { videos, mainVideo, searchOnYoutube, playVideo } = this.props;

        return (
            <div className='row'>
                <Header
                    searchOnYoutube={searchOnYoutube}
                />
                <div className="row">
                    <VideoPlay video={mainVideo}/>
                    <VideoGroup
                        videos={videos}
                        playVideo={playVideo}
                    />
                </div>
            </div>
        )
    }
}

export default Home
