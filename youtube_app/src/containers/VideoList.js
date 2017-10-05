import React from 'react'
import { connect } from 'react-redux'
import VideoListItem from './VideoListItem'

let VideoList = (props) => {
    return (
        <ul>
            {props.videoList.map((video) =>
                <VideoListItem key={ video.id.videoId } video={ video } />
            )}
        </ul>
    );

};

function mapStateToProps(state){
    return {
        videoList: state.videoList,
    };
}

VideoList = connect(mapStateToProps)(VideoList);

export default VideoList
