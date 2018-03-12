import React, { Component } from 'react';
import './App.css';
import YouTube from "react-yt";

class Player extends Component {

    render() {
        return (
            <div style={{paddingLeft:50, paddingTop:50}} className={'pull-left'}>
                <YouTube
                    videoId={this.props.match.params.id}
                    autoplay={true}/>
            </div>
        );
    }
}


export default Player;