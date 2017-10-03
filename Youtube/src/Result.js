import React, { Component } from 'react';
import { Media, Well, Col } from 'react-bootstrap';
import PropTypes from 'prop-types';
import './Result.css';

class Result extends Component {

    static propTypes = {
        handleVideoPlay: PropTypes.func.isRequired,
        result: PropTypes.object.isRequired
    }

    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(videoSrc) {
        this.props.handleVideoPlay(videoSrc);
    }

    render() {

        const video = this.props.result;

        const videoSrc = `https://www.youtube.com/embed/${video.id.videoId}?autoplay=1`;

        return (
            <Col xs={6} md={3}>
                <div>
                    <Well className="result-container">
                        <Media >
                            <img
                                onClick={() => this.handleClick(videoSrc)}
                                src={video.snippet.thumbnails.high.url}
                                alt={videoSrc}
                            />

                            <Media.Body className="media-body">
                                <Media.Heading>
                                    <a
                                        id="title"
                                        onClick={() => this.handleClick(videoSrc)}
                                    >
                                        {video.snippet.title}
                                    </a>
                                </Media.Heading>
                            </Media.Body>
                        </Media>
                    </Well>


                </div>
            </Col>
        );
    }
}

export default Result;
