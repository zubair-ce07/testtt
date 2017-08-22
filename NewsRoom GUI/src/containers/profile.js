import React, { Component } from 'react';
import { connect } from 'react-redux';
import { userProfile } from '../actions';
import { reactLocalStorage } from 'reactjs-localstorage';
import ProfileForm from '../components/profile_form';
import UserInterests from './user_interests';
import _ from 'lodash';


class Profile extends Component {
    componentDidMount(){
        const token = reactLocalStorage.get('token', "");
        if (token){
            this.props.userProfile(token);
        }
        else
        {
            this.props.history.push('/login');
        }
    }

    render() {
        
        if (_.isEmpty(this.props.user))
        {
            return <div>Loading...</div>
        }
        const { user:{ email, first_name, last_name } } = this.props;
        return(
            <div>
            <ProfileForm initialValues={ { email,  first_name, last_name } } />
            <br />
            <UserInterests />
            </div>
        );
    }
}


function mapStateToProps ({ user }){
    return { user };
}

export default connect(mapStateToProps, { userProfile })(Profile);