import React, {Component} from 'react';
import {connect} from "react-redux";

import {MovieList} from './movies_list';
import {setActivePage} from '../actions/active_page_actions';
import {
    addToWatchlist,
    removeFromWatchlist,
    fetchToWatchList,
    fetchWatchedList,
    fetchUpcomingList
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

    updateContentAndSetActivePage(){
        if (this.props.match.params.status === "to-watch") {this.props.fetchToWatchList(); this.props.setActivePage(TOWATCH);}
        if (this.props.match.params.status === "watched") {this.props.fetchWatchedList(); this.props.setActivePage(WATCHED);}
        if (this.props.match.params.status === "upcoming") {this.props.fetchUpcomingList(); this.props.setActivePage(UPCOMING);}
    }

    render() {
        return <div className="page-content row">
            <div className="col-md-2"/>
            <div className="col-md-8">
                {this.props.match.params.status === "watched" &&
                <MovieList movies={this.props.watched_list} addToWatchlist={this.props.addToWatchlist}
                           removeFromWatchlist={this.props.removeFromWatchlist}/>}
                {this.props.match.params.status === "to-watch" &&
                <MovieList movies={this.props.to_watch_list} addToWatchlist={this.props.addToWatchlist}
                           removeFromWatchlist={this.props.removeFromWatchlist}/>}
                {this.props.match.params.status === "upcoming" &&
                <MovieList movies={this.props.upcoming_list} addToWatchlist={this.props.addToWatchlist}
                           removeFromWatchlist={this.props.removeFromWatchlist}/>}
            </div>
        </div>
    }
}

function mapStateToProps({auth_user: {isAuthenticated}, to_watch_list, watched_list, upcoming_list}) {
    return {isAuthenticated, to_watch_list, watched_list, upcoming_list};
}

export default connect(mapStateToProps, {
    fetchToWatchList,
    fetchWatchedList,
    addToWatchlist,
    removeFromWatchlist,
    fetchUpcomingList,
    setActivePage
})(WatchlistPage);
