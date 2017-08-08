import React from 'react';
import SearchList from './search_list';
import YoutubePlayer from './youtube_player';
import $ from 'jquery';
import { Navbar, Grid, Row, Col } from 'react-bootstrap'


class YouTubeApp extends React.Component
{
    constructor(props)
    {
        super(props);
        this.setVidId = this.setVidId.bind(this);
        this.setVidDesc = this.setVidDesc.bind(this);
        this.setVidTitle = this.setVidTitle.bind(this);
        this.updatePlayerDimensions = this.updatePlayerDimensions.bind(this);
        this.state = {'videoId': '', 'videoDesc': '',
                      'videoTitle': '', 'show': false};
    }

    setVidId(videoId)
    {
        this.setState({'videoId': videoId, 'show': true});
    }

    setVidDesc(videoDesc)
    {
        this.setState({'videoDesc': videoDesc});
    }

    setVidTitle(videoTitle)
    {
        this.setState({'videoTitle': videoTitle});
    }

    updatePlayerDimensions()
    {
        let width = 0;
        const aspectRatio = 0.5736;
    
        if($(window).width() < 1200 && $(window).width() > 990)
            width = 420;
        else if($(window).width() <= 990 && $(window).width() > 755)
            width = 600;
        else if($(window).width() <= 755)
            width = 380;
        else
            width = 530;

        this.setState({'playerWidth': width, 'playerHeight': width * aspectRatio});
    }

    componentDidMount()
    {
        this.updatePlayerDimensions();
        window.addEventListener("resize", this.updatePlayerDimensions);
    }

    render()
    {
        return (
            <div>
                <Navbar inverse collapseOnSelect>
                    <Navbar.Header>
                        <Navbar.Brand>
                            <a>MiniTube</a>
                        </Navbar.Brand>
                        <Navbar.Toggle />
                    </Navbar.Header>
                </Navbar>
                <Grid>
                    <Row>
                        <Col md={7}>
                            <YoutubePlayer title={this.state.videoTitle} desc={this.state.videoDesc}
                                     id={this.state.videoId} show={this.state.show}
                                     height={this.state.playerHeight} width={this.state.playerWidth}/>
                        </Col>
                        <Col md={5}>
                            <SearchList setVidTitle={this.setVidTitle}
                            setVidDesc={this.setVidDesc} setVidId={this.setVidId}
                            items={this.state.items} nextPage={this.nextPage}
                            prevPage={this.prevPage}/>
                        </Col>
                    </Row>
                </Grid>
            </div>
        )
    }
}

export default YouTubeApp;