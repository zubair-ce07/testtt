import React, {Component} from 'react';
import {connect} from 'react-redux';

import UserUpdateModal from './user_update_modal';
import {getUserPhoto} from '../utils/utils';
import {fetchUser, sendFollowRequest} from '../actions/user_actions';


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
                <div className="col-md-6">
                    <div className="profile-card row">
                        <div className="col-md-4 p-0">
                            <img src={getUserPhoto(user_profile.photo)} height={200} width={180}
                                 className="float-right rounded-circle"/>
                        </div>
                        <div className="col-md-5 mt-auto mb-3">
                            <h4>
                                <i className="fa fa-user"/> {`${user_profile.first_name} ${user_profile.last_name}`}
                            </h4>
                            <h5><i className="fa fa-calendar"/> {user_profile.date_of_birth}</h5>
                            <h5><i className="fa fa-envelope"/> {user_profile.email}</h5>
                        </div>
                        <div className="col-md-3 my-auto">
                            {this.props.user.id === user_profile.id &&
                                <UserUpdateModal buttonLabel="Update" user={user_profile.id}/>
                            }
                            {this.props.user.id !== user_profile.id &&
                                <button onClick={() => this.sendFollowRequest()}
                                    className={`btn btn-secondary ${user_profile.relation !== null? 'disabled': ''}`}>
                                {user_profile.relation === null? 'Follow' :
                                    user_profile.relation === 'followed'? 'Followed': 'Request Sent'}
                            </button>}
                        </div>
                    </div>
                </div>
            </div>
            }
        </div>;
    }

    sendFollowRequest(){
        if(this.props.user_profile.relation === null)
            this.props.sendFollowRequest(this.props.user_profile.id)
    }
}

function mapStateToProps({auth_user: {isAuthenticated, user}, user_profile}, ownProps) {
    if(user_profile !== null && ownProps.match.params.user_id !== user_profile.id.toString())
        user_profile = null;

    if(user.id.toString() === ownProps.match.params.user_id)
            user_profile = user;

    return {isAuthenticated, user, user_profile};
}

export default connect(mapStateToProps, {fetchUser, sendFollowRequest})(ProfilePage);
