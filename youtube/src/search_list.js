import React from 'react';
import axios from 'axios';
import SearchBar from './search_bar'
import { ListGroup, ListGroupItem,
         Row, Image, Col, Button,
         ButtonGroup } from 'react-bootstrap';


class SearchList extends React.Component
{
    constructor(props)
    {
        super(props);
        this.nextPage = this.nextPage.bind(this);
        this.prevPage = this.prevPage.bind(this);
        this.setQuery = this.setQuery.bind(this);
        this.search = this.search.bind(this);
        this.state = {'query': '', 'items': [],
                      'nextPageToken': '', 'prevPageToken': ''}
    }

    itemSelect(videoId, videoDesc, videoTitle)
    {
        this.props.setVidId(videoId);
        this.props.setVidDesc(videoDesc);
        this.props.setVidTitle(videoTitle);
    }

    setQuery(e)
    {
        this.setState({'query': e.target.value});
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
            this.setState({'items': res.data.items,
                           'nextPageToken': res.data.nextPageToken,
                           'prevPageToken': res.data.prevPageToken});
            console.log(this.state.items);
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

    render()
    {
        let results = this.state.items;
        if (results && results.length)
        {
            return (
                <div>
                    <SearchBar query={this.state.query} 
                     setQuery={this.setQuery} search={this.search}/>

                    <ListGroup>
                        {
                            results.map(result => {
                                return (
                                    <ListGroupItem key={results.indexOf(result)} onClick={() =>
                                                        this.itemSelect(result.id.videoId,
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
                    </ListGroup>
                    <ButtonGroup justified>
                        <ButtonGroup>
                            <Button type="submit" onClick={this.prevPage}>Prev</Button>
                        </ButtonGroup>
                        <ButtonGroup>
                            <Button type="submit" onClick={this.nextPage}>Next</Button>
                        </ButtonGroup>
                    </ButtonGroup>
                </div>
            )
        }
        else
            return(
                <div>
                    <Row>
                        <SearchBar setQuery={this.setQuery} search={this.search} />
                    </Row>
                    <Row>
                        <h2>Enter a Search Query</h2>
                    </Row>                   
                </div>
            )
    }
}

export default SearchList;