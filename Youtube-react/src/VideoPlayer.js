import React, { Component } from 'react';
import YoutubePlayer from 'react-youtube-player';

  const opts = {
    height: 690,
    width: 1080,
    'margin-left':35,
  };

class VideoPlayer extends Component{

    createPlayer(){
        let player = [];
        if(this.props.videoId!==''){
            player.push(
                <div style={opts}>
                    <YoutubePlayer
                        videoId={this.props.videoId}
                        opts={opts}
                        playbackState='unstarted'
                        configuration={
                            {
                                showinfo: 0,
                                controls: 1
                            }
                        }
                    />
                </div>

            );
        }
        return player;
    }

    render(){
        return (
            <div style={opts}>{this.createPlayer()}</div>
        )
    }
}

export {VideoPlayer};
