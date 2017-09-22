import _ from 'lodash';
import React, {Component} from 'react';
import {connect} from "react-redux";
import Waypoint from 'react-waypoint';

import {fetchActivities} from '../actions/activities_actions';
import {fetchMore} from '../actions/more_content_actions';
import {setActivePage} from '../actions/active_page_actions';
import {addToWatchlist, removeFromWatchlist} from "../actions/watchlist_actions";
import Activity from './activity_item'
import {HOME} from "../utils/page_types";


class HomePage extends Component {
    componentWillMount() {
        if (!this.props.isAuthenticated) this.props.history.push('/login/');
        this.props.setActivePage(HOME);
        this.props.fetchActivities()
    }

    renderActivities() {
        return _.map(this.props.activity_list.activities, activity => {
            return <Activity activity={activity} key={activity.id}
                             addToWatchlist={(movie_id) => this.props.addToWatchlist(movie_id)}
                             removeFromWatchlist={(movie_id) => this.props.removeFromWatchlist(movie_id)}/>;
        });
    }

    loadMore() {
        if (this.props.activity_list.next !== null) {
            this.props.fetchMore(this.props.activity_list.next);
        }
    }

    render() {
        return <div className="page-content row">
            <div className="col-md-2"/>
            <div className="col-md-8">
                {!this.props.activity_list.isFetching && this.props.activity_list.activities.length === 0 &&
                <h4 className="text-center my-5">No Result Found</h4>}
                {this.renderActivities()}
                {this.props.activity_list.isFetching ? <h4 className="text-center my-5">Loading...</h4>
                    : <Waypoint onEnter={this.loadMore.bind(this)} bottomOffset="-100%"/>}
            </div>
        </div>
    }
}

function mapStateToProps({auth_user: {isAuthenticated}, activity_list}) {
    return {isAuthenticated, activity_list};
}

export default connect(mapStateToProps, {
    fetchActivities,
    addToWatchlist,
    removeFromWatchlist,
    setActivePage,
    fetchMore
})(HomePage);
