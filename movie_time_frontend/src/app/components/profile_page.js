import React, {Component} from 'react';
import {connect} from 'react-redux';

import UserCard from './user_item';
import {fetchUser} from '../actions/user_actions';


class ProfilePage extends Component {
    componentWillMount() {
        if (!this.props.isAuthenticated) this.props.history.push('/login/');
        this.props.fetchUser(this.props.match.params.user_id);
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
                </div>
            </div>
            }
        </div>;
    }
}

function mapStateToProps({auth_user: {isAuthenticated, user}, user_profile}, ownProps) {
    if(user_profile !== null && ownProps.match.params.user_id !== user_profile.id.toString())
        user_profile = null;

    if(user.id.toString() === ownProps.match.params.user_id)
            user_profile = user;

    return {isAuthenticated, user, user_profile};
}

export default connect(mapStateToProps, {fetchUser})(ProfilePage);
