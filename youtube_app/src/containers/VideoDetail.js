import React from 'react'
import { connect } from 'react-redux'

let VideoDetail = (props) => {
    const video = props.selectedVideo;
    const videoUrl = "https://www.youtube.com/embed/" + video.id.videoId;

    return (
        <div>
            <div>
                <iframe src={ videoUrl } title={ video.snippet.title }></iframe>
            </div>
            <div>
                <div>
                    { video.snippet.title }
                </div>
                <div>
                    { video.snippet.description }
                </div>
                <div>
                    { video.snippet.publishedAt }
                </div>

            </div>
        </div>
    );
}

function mapStateToProps(state){
    return {
        selectedVideo: state.selectedVideo
    };
}

VideoDetail = connect(mapStateToProps)(VideoDetail);

export default VideoDetail
