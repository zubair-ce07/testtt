import React from 'react';

const VideoItem = (props) => {
    const video = props.video;
    const onUserSelected = props.onUserSelected;
    const imageUrl = video.snippet.thumbnails.default.url;

    return (
        <div onClick={() => onUserSelected(video)} className="related-video-list">
            <div className="media">
                <div className="media-left">
                    <img className="media-object" src={imageUrl} alt="video thumbnail" />
                </div>
                <div className="media-body">
                    <div className="media-heading">{video.snippet.title}</div>
                </div>
            </div>
        </div>
    );
}

export default VideoItem;
