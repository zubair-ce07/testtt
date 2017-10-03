import React, { Component } from 'react';
import { Grid, Row } from 'react-bootstrap';
import PropTypes from 'prop-types';
import Result from './Result.js';


class VideoPlayer extends Component {

    static propTypes = {
        videoSrc: PropTypes.string.isRequired
    }

    render() {
        return (
            <div>
                <iframe
                    title="playerFrame"
                    className="player"
                    src={this.props.videoSrc}
                    frameBorder="0"
                    allowFullScreen
                    width="100%"
                    height="500"
                />
            </div>
        );
    }
}


class VideoList extends Component {

    static propTypes = {
        videos: PropTypes.array.isRequired,
    }


    constructor(props) {
        super(props);
        this.state = {
            videoSrc: '',
        }
        this.PlayVideo = this.PlayVideo.bind(this);
    }

    playVideo(videoSrc) {
        this.setState({
            videoSrc: videoSrc
        })
    }

    render() {
        return (
            <div>
                {this.state.videoSrc &&
                    < VideoPlayer
                        videoSrc={this.state.videoSrc}
                    />
                }
                <Grid>
                    <Row>
                        {this.props.videos.map(video =>
                            <Result
                                key={video.id.videoId}
                                result={video}
                                handleVideoPlay={this.playVideo}
                            />
                        )
                        }
                    </Row>

                </Grid>
            </div>
        );
    }
}

export default VideoList;
