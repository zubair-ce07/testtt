import React, { Component } from 'react';
import VideoGroupItem from './VideoGroupItem'
import PropTypes from 'prop-types';

class VideoGroup extends Component {
    // Video group component
    static propTypes = {
        videos: PropTypes.array.isRequired,
        playVideo: PropTypes.func.isRequired
    };

    render() {
        const { videos, playVideo } = this.props;
        const videoItems = videos.map((videoItem) => {
            return (
                <VideoGroupItem
                    key={videoItem.id.videoId}
                    videoItem={videoItem}
                    playVideo={playVideo}
                />
            );
        });

        return (
            <div className="col-md-4">
                <ul className="list-group">
                    {videoItems}
                </ul>
            </div>
        );
    }
}

export default VideoGroup
