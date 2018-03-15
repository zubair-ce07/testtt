import React, { Component } from 'react';
import './App.css';
import * as youtubeSearch from 'youtube-search';
import { Link } from 'react-router-dom'
import PropTypes from 'prop-types';

var opts: youtubeSearch.YouTubeSearchOptions = {
    maxResults: 10,
    key: 'AIzaSyDbh9um58oWl8wptkdL7IvVtQcbJuDtBCs'
};

class List extends Component {
    constructor(props) {
        super(props);

        this.handleDataRetrieval = this.handleDataRetrieval.bind(this);
    }
    handleDataRetrieval(results) {

        this.props.onDataRetrieval(results)
    }
    getData(){

        this.props.onLoading(true,'Loading...')
        youtubeSearch(this.props.query, opts, (err, results) => {
            if(err) {
                this.props.onLoading(false,'Something went wrong while fetching data')
                return err
            }
            this.handleDataRetrieval(results)
        });

    }

    componentDidMount() {

        this.getData()
    }

    componentWillReceiveProps(nextProps) {

        if(nextProps.searchText!==this.props.searchText ) this.getData()
    }

    render() {
        return (
            <div >
                <dl>
                    {this.props.items.map(video => {
                        return (
                            <div className={'row'} style={{paddingLeft:50,paddingTop:10}} key={video.id} >
                                <Link to={`/play/${video.id}`} className={'crop'}>
                                    <div className={'col-md-3'}>
                                        <img className={'thumbnail'} src={video.thumbnails.default.url} alt={''}></img>
                                        <br></br>
                                    </div>
                                    <div className={'crop col-md-4'} >
                                        <label style={{color:'black',fontWeight:'bold'}}>{video.title}</label>
                                        {video.description}
                                    </div>
                                </Link>
                            </div>
                        )
                    })}
                </dl>
            </div>

        );
    }


}

List.propTypes = {
    searchText:PropTypes.string,
    query:PropTypes.string,
    onDataRetrieval:PropTypes.func,
    onLoading:PropTypes.func,
    items:PropTypes.array,

};


export default List
