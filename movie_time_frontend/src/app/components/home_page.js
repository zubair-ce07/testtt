import _ from 'lodash';
import React, {Component} from 'react';
import {connect} from "react-redux";

import {fetchActivities} from '../actions/activities_actions';
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
        return _.map(this.props.activities, activity => {
            return <Activity activity={activity} key={activity.id}
                             addToWatchlist={(movie_id) => this.props.addToWatchlist(movie_id)}
                             removeFromWatchlist={(movie_id) => this.props.removeFromWatchlist(movie_id)}/>;
        });
    }

    render() {
        const {activities} = this.props;
        if (_.isEmpty(activities))
            return <div>Loading</div>;

        return <div className="page-content row">
            <div className="col-md-2"/>
            <div className="col-md-8">
                {this.renderActivities()}
            </div>
        </div>
    }
}

function mapStateToProps({auth_user: {isAuthenticated}, activities}) {
    return {isAuthenticated, activities};
}

export default connect(mapStateToProps, {fetchActivities, addToWatchlist, removeFromWatchlist, setActivePage})(HomePage);
