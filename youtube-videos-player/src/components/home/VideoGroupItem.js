import React, { Component } from 'react';
import PropTypes from 'prop-types';

class VideoGroupItem extends Component {
    // Video group component
    
    static propTypes = {
        videoItem: PropTypes.object.isRequired,
        playVideo: PropTypes.func.isRequired
    };

    render() {
        const { videoItem, playVideo } = this.props;
        const imageUrl = videoItem.snippet.thumbnails.default.url;
        const { title:videoTitle, publishedAt:videoPublishedAt } = videoItem.snippet;

        return (
            <li onClick={() => playVideo(videoItem)} className="videos-list-item">
                <div className="video-list media">
                    <div className="media-left">
                        <img
                            className="media-object border-round"
                            alt={videoTitle}
                            src={imageUrl}
                        />
                    </div>
                    <div className="media-body">
                        <div className="media-heading white-large">{videoTitle}</div>
                        <div className="video-publisher-date grey-small">
                            Published on: {(new Date(videoPublishedAt)).toDateString()}
                        </div>
                    </div>
                </div>
            </li>
        );
    }
}

export default VideoGroupItem
