import React, {Component} from 'react';
import {connect} from "react-redux";
import Waypoint from 'react-waypoint';

import {MovieList} from './movies_list';
import {fetchMore} from '../actions/more_content_actions';
import {setActivePage} from '../actions/active_page_actions';
import {
    addToWatchlist,
    removeFromWatchlist,
    fetchWatchList
} from "../actions/watchlist_actions";
import {UPCOMING, WATCHED, TOWATCH} from "../utils/page_types";


class WatchlistPage extends Component {
    componentWillMount() {
        if (!this.props.isAuthenticated) this.props.history.push('/login/');
        this.updateContentAndSetActivePage();
    }

    componentDidUpdate(prevProps) {
        if (this.props.match.params.status !== prevProps.match.params.status) {
            this.updateContentAndSetActivePage();
        }
    }

    updateContentAndSetActivePage() {
        const {status} = this.props.match.params;
        if (status === "to-watch") {
            this.props.fetchWatchList(status);
            this.props.setActivePage(TOWATCH);
        }
        if (status === "watched") {
            this.props.fetchWatchList(status);
            this.props.setActivePage(WATCHED);
        }
        if (status === "upcoming") {
            this.props.fetchWatchList(status);
            this.props.setActivePage(UPCOMING);
        }
    }

    loadMore() {
        if (this.props.movie_watchlist.next !== null)
            this.props.fetchMore(this.props.movie_watchlist.next);
    }

    render() {
        return <div className="page-content row">
            <div className="col-md-2"/>
            <div className="col-md-8">
                {!this.props.movie_watchlist.isFetching && this.props.movie_watchlist.movies.length === 0 &&
                <h4 className="text-center my-5">No Result Found</h4>}
                <MovieList movies={this.props.movie_watchlist.movies} addToWatchlist={this.props.addToWatchlist}
                           removeFromWatchlist={this.props.removeFromWatchlist}/>
                {this.props.movie_watchlist.isFetching ? <h4 className="text-center my-5">Loading...</h4>
                    : <Waypoint onEnter={() => this.loadMore()} bottomOffset="-100%"/>}
            </div>
        </div>
    }
}

function mapStateToProps({auth_user: {isAuthenticated}, movie_watchlist}) {
    return {isAuthenticated, movie_watchlist};
}

export default connect(mapStateToProps, {
    fetchWatchList,
    addToWatchlist,
    removeFromWatchlist,
    setActivePage,
    fetchMore
})(WatchlistPage);
