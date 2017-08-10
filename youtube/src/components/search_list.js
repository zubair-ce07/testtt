import React from 'react';
import axios from 'axios';
import SearchBar from './search_bar';
import {youtubeConfig} from '../config';
import { ListGroup, ListGroupItem,
         Row, Image, Col,
         Pager } from 'react-bootstrap';


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
        const base_url = youtubeConfig.youtubeAPIUrl;
        const key =  youtubeConfig.apiKey;
        const part = youtubeConfig.part;
        const query = this.state.query;
        const type = youtubeConfig.type;
        const videoCaption = youtubeConfig.videoCaption;
        const totalResults = youtubeConfig.totalResults;

        return (
             base_url + '?part=' + part +
             '&q=' + query + '&type=' + type +
             '&videoCaption=' + videoCaption +
             '&maxResults=' + totalResults +
             '&order=viewCount&key=' + key
        );
    }

    sendRequest(getRequest)
    {
        axios.get(getRequest)
        .then(res => {
            this.setState({'items': res.data.items,
                           'nextPageToken': res.data.nextPageToken,
                           'prevPageToken': res.data.prevPageToken});
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
                                                <Image alt={result.snippet.name} responsive
                                                    src={result.snippet.thumbnails.default.url}/>
                                            </Col>
                                            <Col xs={9}>
                                                <h4> {result.snippet.title}</h4>
                                            </Col>
                                        </Row>
                                    </ListGroupItem>
                                );
                            })
                        }
                    </ListGroup>
                    <Pager>
                        <Pager.Item previous onClick={this.prevPage}>&larr; Previous</Pager.Item>
                        <Pager.Item next onClick={this.nextPage}>Next &rarr;</Pager.Item>
                    </Pager>
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