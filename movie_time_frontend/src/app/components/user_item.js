import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Link} from 'react-router-dom';

import UserUpdateModal from './user_update_modal';
import {getUserPhoto} from '../utils/utils';
import {sendFollowRequest} from '../actions/user_actions';


class UserCard extends Component {

    render() {
        const {user_profile} = this.props;
        const {show_actions} = this.props;

        return <div className="profile-card row">
            <div className="col-md-4 p-0">
                <img src={getUserPhoto(user_profile.photo)} height={200} width={180}
                     className="float-right rounded-circle"/>
            </div>
            <div className="col-md-5 mt-auto mb-3">
                <Link to={`/users/${user_profile.id}/`}><h4>
                    <i className="fa fa-user"/> {`${user_profile.first_name} ${user_profile.last_name}`}
                </h4></Link>
                <h5><i className="fa fa-calendar"/> {user_profile.date_of_birth}</h5>
                <h5><i className="fa fa-envelope"/> {user_profile.email}</h5>
            </div>
            {show_actions && <div className="col-md-3 my-auto">
                {this.props.user.id === user_profile.id &&
                    <UserUpdateModal buttonLabel="Update" user={user_profile.id}/>
                }
                {this.props.user.id !== user_profile.id &&
                    <button onClick={() => this.sendFollowRequest()}
                        className={`btn btn-secondary ${user_profile.relation !== null? 'disabled': ''}`}>
                    {user_profile.relation === null? 'Follow' :
                        user_profile.relation === 'followed'? 'Followed': 'Request Sent'}
                </button>}
            </div>}
        </div>;
    }

    sendFollowRequest(){
        if(this.props.user_profile.relation === null)
            this.props.sendFollowRequest(this.props.user_profile.id)
    }
}

function mapStateToProps({auth_user: {isAuthenticated, user}}) {
    return {isAuthenticated, user};
}

export default connect(mapStateToProps, {sendFollowRequest})(UserCard);
