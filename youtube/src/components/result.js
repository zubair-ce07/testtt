import React from 'react';
import VideoThumbnail from './videoitem'

class Result extends React.Component{
  constructor(props){
    super(props);
    this.state = {prevPropsList: props,
                  videoList: [],
                  isPlaying: false,
                  getURL: this.playVideo,
                  url: ""
                  };
    this.playVideo = this.playVideo.bind(this);
  }

  playVideo = (link) =>
  {
    this.setState({isPlaying: true, url: link});
  }

  static getDerivedStateFromProps(props, state) {
    if (props !== state.prevPropsList)
    {
        let videos = props.videos.map(video => {
          return (
            <div key={video.etag}>
              <VideoThumbnail video={video} playerCheck={state.isPlaying} videoURL={(url) => state.getURL(url)}/>
              <hr className="my-4"/>
          </div>
        );}
      );
      return {videoList: videos, prevPropsList: props, isPlaying: false}
    }
    return null;
  }

  render()
  {
    return(
      <div className="container mt-5">
        <div className="row">
          {this.state.isPlaying ?
          <div className="col-md-8">
            <iframe className="video-player"
              src={this.state.url}>
            </iframe>
          </div>
          :
          null
        }
          <div className={this.state.isPlaying ? "col-md-4" : ""}>
               {this.state.videoList}
          </div>
        </div>
      </div>
    )
  }
};

export default Result;
