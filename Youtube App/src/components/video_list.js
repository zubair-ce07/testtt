import React from 'react';
import VideoItem from './video_item';

const VideoList = (props) => {
    const videoItems = props.videos.map((video) => {
        return (
            <VideoItem key={video.etag} video={video} onUserSelected={props.onVideoSelect} />
        );
    });

    return (
        <ul>{videoItems}</ul>
    );
};

export default VideoList;
