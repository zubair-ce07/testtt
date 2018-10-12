import _ from 'underscore';
import React, { Component } from 'react';
import PropTypes from 'prop-types';

class VideoPlay extends Component {
    // Play video component
    static propTypes = {
        video: PropTypes.object.isRequired
    };

    render() {
        const youtubeVideoPlayUrl = 'https://www.youtube.com/embed/';
        const video = this.props.video;

        // Checks if there is no video to play
        if(_.isEmpty(video)){
            return <div>Loading...</div>;
        }

        const videoUrl = `${youtubeVideoPlayUrl}${video.id.videoId}`;
        const { title:videoTitle, description:videoDescription } = video.snippet;

        return (
            <div className="video-play col-md-8 col-sm-12">
                <div className="embed-responsive embed-responsive-16by9">
                    <iframe
                        className="embed-responsive-item"
                        src={videoUrl}
                        title={videoTitle}
                    >videoTitle</iframe>
                </div>
                <div className="details">
                    <div className='left-allign'>{videoTitle}</div>
                    <div className='left-allign grey-small'>{videoDescription}</div>
                </div>
            </div>
        )
    }
}

export default VideoPlay
