import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Thumbnail, Grid, Row, Col } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import _ from 'lodash';
import { fetchSearchNews } from '../actions'
import SearchBar from '../components/search_bar'
import NewsThumbnailList from '../components/news_thumbnail_list';


class NewsList extends Component {

    componentDidMount(){
        const query = this.props.match.params.query;
        this.props.fetchSearchNews(query);
    }

    render(){
        if (!this.props.searchNews){
            return <div>Loading...</div>
        }
        return ( 
            <div>
                <SearchBar />
                <NewsThumbnailList news_list={ this.props.searchNews } />
            </div>
        );
    }
}

function mapStateToProps(state) {
    return { 
        searchNews: state.searchNews,
    };
}


export default connect(mapStateToProps, { fetchSearchNews })(NewsList);