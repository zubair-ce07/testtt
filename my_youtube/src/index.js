import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import axios from 'axios';
import YouTube from 'react-youtube';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import { ListGroup, ListGroupItem, Grid, Row, Image, Col,
         Jumbotron, TabContainer, Navbar, FormGroup,
         FormControl, Button, Form, ButtonGroup,
         ButtonToolbar } from 'react-bootstrap';


class SearchList extends React.Component
{
    constructor(props)
    {
        super(props);
        // this.handleClick = this.handleClick.bind(this);
    }

    handleClick(videoId, videoDesc, videoTitle)
    {
        this.props.setVidId(videoId);
        this.props.setVidDesc(videoDesc);
        this.props.setVidTitle(videoTitle);
    }

    render()
    {
        let results = this.props.items;

        if (results)
        {
            return (
                <ListGroup>
                    {
                        results.map(result => {
                            return (
                                <ListGroupItem key={results.indexOf(result)} onClick={() =>
                                                    this.handleClick(result.id.videoId,
                                                                    result.snippet.description,
                                                                    result.snippet.title)}>
                                    <Row>
                                        <Col xs={3}>
                                            <Image className="list-group-item-text"
                                                alt={result.snippet.name} responsive
                                                src={result.snippet.thumbnails.default.url}/>
                                        </Col>
                                        <Col xs={9}>
                                            <h4> {result.snippet.title}</h4>
                                        </Col>
                                    </Row>
                                </ListGroupItem>
                            )
                        })
                    }
                    <ButtonToolbar>
                        <ButtonGroup>
                            <Button type="submit" onClick={this.props.prevPage}>Prev</Button>
                            <Button type="submit" onClick={this.props.nextPage}>Next</Button>
                        </ButtonGroup>
                    </ButtonToolbar>
                </ListGroup>
            )
        }
        else
            return(
                <h2>Enter a Search Query</h2>
            )
    }
}

class YoutubePlayer extends React.Component {
  render() {
    const opts = {
      height: '304',
      width: '530',
    };

    if(this.props.show)
    {
        return (
            <div>
                <Jumbotron>
                    <YouTube
                        videoId={this.props.id}
                        opts={opts}
                        onReady={this._onReady}
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

  _onReady(event) {
    // access to player in all event handlers via event.target
    event.target.pauseVideo();
  }
}

class MiniYoutube extends React.Component
{
    constructor(props)
    {
        super(props);
        this.search = this.search.bind(this);
        this.nextPage = this.nextPage.bind(this);
        this.prevPage = this.prevPage.bind(this);
        this.setQuery = this.setQuery.bind(this);
        this.setVidId = this.setVidId.bind(this);
        this.setVidDesc = this.setVidDesc.bind(this);
        this.setVidTitle = this.setVidTitle.bind(this);
        this.state = {'query': '', 'videoId': '', 'videoDesc': '',
                      'videoTitle': '', 'items': [], 'show': false,
                      'nextPageToken': ''};
    }

    setQuery(e)
    {
        this.setState({'query': e.target.value, 'items': []});
    }

    _prepareGETRequest()
    {
        const base_url = 'https://www.googleapis.com/youtube/v3/search';
        const key =  'AIzaSyDMyxo6mKMTtCiI6t7JoItSwI2NjJGHzDk';
        const part = 'snippet';
        const query = this.state.query;
        const type = 'video'
        const videoCaption = 'closedCaption'
        const totalResults = 5;

        let getRequest = base_url + '?part=' + part +
                         '&q=' + query + '&type=' + type +
                         '&videoCaption=' + videoCaption +
                         '&maxResults=' + totalResults +
                         '&order=viewCount';

        getRequest += '&key=' + key;

        return getRequest;
    }

    sendRequest(getRequest)
    {
        axios.get(getRequest)
        .then(res => {
            this.setState({'items': res.data.items});
            this.setState({'nextPageToken': res.data.nextPageToken});
            this.setState({'prevPageToken': res.data.prevPageToken});
        });
    }

    search(e)
    {
        let getRequest = this._prepareGETRequest();
        this.sendRequest(getRequest);
        e.preventDefault();
    }

    nextPage(e)
    {
        let getRequest = this._prepareGETRequest();
        if(this.state.nextPageToken)
        {
            getRequest += '&pageToken=' + this.state.nextPageToken;
        }
        this.sendRequest(getRequest);
        e.preventDefault();
    }

    prevPage(e)
    {
        let getRequest = this._prepareGETRequest();
        if(this.state.prevPageToken)
        {
            getRequest += '&pageToken=' + this.state.prevPageToken;
        }
        this.sendRequest(getRequest);
        e.preventDefault();
    }

    setVidId(videoId)
    {
        this.setState({'videoId': videoId});
        this.setState({'show': true});
    }

    setVidDesc(videoDesc)
    {
        this.setState({'videoDesc': videoDesc});
    }

    setVidTitle(videoTitle)
    {
        this.setState({'videoTitle': videoTitle});
    }

    render()
    {
        return (
            <div>
                <Navbar inverse collapseOnSelect>
                    <Navbar.Collapse>
                    <form onSubmit={this.search}>
                        <Navbar.Form pullRight>
                            <FormGroup>
                                <FormControl type="text" onChange={this.setQuery} placeholder="Search" />
                                </FormGroup>
                                {' '}
                            <Button type="submit" onClick={this.search}>Search</Button>
                        </Navbar.Form>
                    </form>
                    </Navbar.Collapse>
                </Navbar>
                <Grid>
                    <Row>
                        <Col md={7}>
                            <YoutubePlayer title={this.state.videoTitle} desc={this.state.videoDesc}
                                     id={this.state.videoId} show={this.state.show}/>
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

ReactDOM.render(
  <MiniYoutube/>,
  document.getElementById('root'),
);