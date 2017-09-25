import _ from 'lodash';
import React, {Component} from 'react';
import {connect} from 'react-redux';
import Waypoint from 'react-waypoint';

import Activity from './activity_item';
import UserCard from './user_item';
import {fetchUserActivities} from '../actions/activities_actions';
import {fetchUser} from '../actions/user_actions';
import {fetchMore} from '../actions/more_content_actions';


class ProfilePage extends Component {
    componentWillMount() {
        if (!this.props.isAuthenticated) this.props.history.push('/login/');
        this.props.fetchUser(this.props.match.params.user_id);
        this.props.fetchUserActivities(this.props.match.params.user_id);
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
        const {user_profile} = this.props;

        return <div className="page-content">
            {user_profile === null && <h3>Loading...</h3>}
            {user_profile !== null &&
            <div className="row">
                <div className="col-md-3"/>
                <div className="col-md-6 mt-3">
                    <UserCard user_profile={user_profile} show_actions={true}/>
                    {!this.props.activity_list.isFetching && this.props.activity_list.activities.length === 0 &&
                    <h4 className="text-center my-5">No Activity Yet</h4>}
                    {this.renderActivities()}
                    {this.props.activity_list.isFetching ? <h4 className="text-center my-5">Loading...</h4>
                        : <Waypoint onEnter={this.loadMore.bind(this)} bottomOffset="-100%"/>}
                </div>
            </div>
            }
        </div>;
    }
}

function mapStateToProps({auth_user: {isAuthenticated, user}, user_profile, activity_list}, ownProps) {
    if(user_profile !== null && ownProps.match.params.user_id !== user_profile.id.toString())
        user_profile = null;

    if(user.id.toString() === ownProps.match.params.user_id)
            user_profile = user;

    return {isAuthenticated, user, user_profile, activity_list};
}

export default connect(mapStateToProps, {fetchUser, fetchUserActivities, fetchMore})(ProfilePage);
