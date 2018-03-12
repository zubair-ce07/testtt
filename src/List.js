import React, { Component } from 'react';
import './App.css';
import * as youtubeSearch from "youtube-search";
import { Link } from 'react-router-dom'

var opts: youtubeSearch.YouTubeSearchOptions = {
    maxResults: 10,
    key: "AIzaSyDbh9um58oWl8wptkdL7IvVtQcbJuDtBCs"
};



class Search extends Component {

    constructor(props) {
        super(props);
        this.state = {query:''};

        // This binding is necessary to make `this` work in the callback
        this.handleChange = this.handleChange.bind(this);
    }
    render() {

        return (
            <div   style={{paddingLeft:50,paddingTop:10}}  >

                <input id="query" name="query" value={this.state.query}  onChange={this.handleChange} type="text"/>
                <Link to={`/search/${this.state.query}`}><button id="search-button" name="search-button">Search</button></Link>


            </div>

        );


    }

    handleChange(event) {
        this.setState({query: event.target.value});
    }

}


class List extends Component {


    constructor(props) {
        super(props);
        this.state = {
            items: []
        };

        youtubeSearch(this.props.match.params.query, opts, (err, results) => {
            if(err) return console.log(err);
            this.setState({items:results})

        });
    }

    render() {

        return (
            <div >

            <dl>
                {this.state.items.map(video => {
                    return (
                        <div className={'row'} style={{paddingLeft:50,paddingTop:10}} key={video.id}>
                            <Link to={`/play/${video.id}`} className={'crop'}>
                                <div className={"col-md-3 "}>

                                    <img className={"thumbnail"} src={video.thumbnails.default.url} alt="">
                                    </img>
                                    <br></br>

                                </div>
                                <div className={'crop col-md-4'} >
                                    <label style={{color:'black',fontWeight:'bold'}}>{video.title}</label>
                                    {video.description}

                                </div>
                                <div className={'col-md-4 '} >

                                </div>

                            </Link>
                        </div>

                    )
                })
                }
    </dl>
            </div>

        );


    }
}


export {List, Search}
