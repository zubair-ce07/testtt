import React from 'react'
import { showDetail } from '../actions'
import { connect } from 'react-redux'


let VideoListItem = (props) => {
    const { video } = props;
    const imageUrl = video.snippet.thumbnails.default.url;
    return (
        <li>
            <div>
                <div>
                    <div>
                        {video.snippet.title}
                    </div>
                </div>
                <div>
                    <img alt={ video.snippet.title } src={ imageUrl }  onClick={() => props.onClick(video)}/>
                </div>
            </div>
        </li>
    );
};

const mapDispatchToProps = dispatch => {
    return {
        onClick: video => dispatch(showDetail(video))

    }
};

VideoListItem = connect(null, mapDispatchToProps)(VideoListItem);

export default VideoListItem
