import React, {Component} from 'react';
import {connect} from "react-redux";

import {MovieList} from './movies_list';
import {setActivePage} from '../actions/active_page_actions';
import {addToWatchlist, removeFromWatchlist} from "../actions/watchlist_actions";
import {SEARCH} from "../utils/page_types";


class SearchPage extends Component{
    componentWillMount() {
        if (!this.props.isAuthenticated) this.props.history.push('/login/');
        this.props.setActivePage(SEARCH);
    }

    render(){
        return <div className="page-content row">
            <div className="col-md-2"/>
            <div className="col-md-8">
                {this.props.search_results.isFetching? <div className="text-center">Loading...</div>
                : this.props.search_results.movies.length === 0? <div className="text-center">No Results Found</div>
                : <MovieList movies={this.props.search_results.movies} addToWatchlist={this.props.addToWatchlist}
                           removeFromWatchlist={this.props.removeFromWatchlist}/>}
            </div>
        </div>
    }
}

function mapStateToProps({auth_user: {isAuthenticated}, search_results}) {
    return {search_results, isAuthenticated};
}

export default connect(mapStateToProps, {addToWatchlist, removeFromWatchlist, setActivePage})(SearchPage);
