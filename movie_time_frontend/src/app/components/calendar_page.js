import React, {Component} from 'react';
import {connect} from "react-redux";
import DayPicker from 'react-day-picker';
import Waypoint from 'react-waypoint';
import 'react-day-picker/lib/style.css';

import {MovieList} from './movies_list';
import {fetchMore} from '../actions/more_content_actions';
import {addToWatchlist, removeFromWatchlist} from "../actions/watchlist_actions";
import {fetchReleasedOn, requestingWithReleaseDate} from '../actions/explore_actions';
import {setActivePage} from '../actions/active_page_actions';
import {CALENDAR} from "../utils/page_types";


class CalendarPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            day: new Date()
        }
    }

    componentWillMount() {
        if (!this.props.isAuthenticated) this.props.history.push('/login/');
        this.props.setActivePage(CALENDAR);
        const date = new Date();
        this.props.fetchReleasedOn(date.getDate(), date.getMonth() + 1, date.getFullYear());
        this.props.requestingWithReleaseDate();
    }

    onDaySelected(day) {
        this.setState({day: day});
        this.props.fetchReleasedOn(day.getDate(), day.getMonth() + 1, day.getFullYear());
        this.props.requestingWithReleaseDate();
    }

    loadMore() {
        if(this.props.released_on_list.next !== null) {
            this.props.fetchMore(this.props.released_on_list.next);
        }
    }

    render() {
        return <div className="page-content row">
            <div className="col-md-1"/>
            <div className="col-md-8">
                {!this.props.released_on_list.isFetching && this.props.released_on_list.movies.length === 0 &&
                <h4 className="text-center my-5">No Result Found</h4>}
                <MovieList movies={this.props.released_on_list.movies} addToWatchlist={this.props.addToWatchlist}
                           removeFromWatchlist={this.props.removeFromWatchlist}/>
                {this.props.released_on_list.isFetching? <h4 className="text-center my-5">Loading...</h4>
                    : <Waypoint onEnter={this.loadMore.bind(this)} bottomOffset="-100%"/>}
            </div>
            <div className="col-md-3">
                <DayPicker selectedDays={this.state.day} onDayClick={this.onDaySelected.bind(this)}/>
            </div>
        </div>
    }
}

function mapStateToProps({auth_user: {isAuthenticated}, released_on_list}) {
    return {released_on_list, isAuthenticated};
}

export default connect(mapStateToProps, {
    addToWatchlist,
    removeFromWatchlist,
    fetchReleasedOn,
    requestingWithReleaseDate,
    setActivePage,
    fetchMore
})(CalendarPage);
