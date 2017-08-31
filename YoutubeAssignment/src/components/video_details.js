import React, { Component} from 'react';

class VideoDetail extends Component{

    render(){
        const video = this.props.videoItem;
        if(!video){
            return <div></div>;
        }
        const videoSrc = `https://www.youtube.com/embed/${video.id.videoId}`;

        return(
            <div className="video-detail col-md-8">
                <div className="embed-responsive embed-responsive-16by9">
                    <iframe className="embed-responsive-item" src={videoSrc} />
                </div>
                <div className="details">
                    <div>{video.snippet.title}</div>
                    <div>{video.snippet.description}</div>
                </div>
            </div>
        );
    }//render

}//class

export default VideoDetail;