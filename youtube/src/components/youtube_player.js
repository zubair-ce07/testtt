import React from 'react';
import YouTube from 'react-youtube';
import {Jumbotron} from 'react-bootstrap';


class YoutubePlayer extends React.Component {
  render() {
    const opts = {
      height: this.props.height,
      width: this.props.width,
      playerVars: {
        autoplay: 1,
        start: 1
      }
    };

    if(this.props.show)
    {
        return (
            <div>
                <Jumbotron>
                    <YouTube
                        videoId={this.props.id}
                        opts={opts}
                    />
                    <h2>{this.props.title}</h2>
                    <h4>
                        {this.props.desc}
                    </h4>
                </Jumbotron>
            </div>
        );
    }
    else
        return (
            <div></div>
        )
  }
}

export default YoutubePlayer;