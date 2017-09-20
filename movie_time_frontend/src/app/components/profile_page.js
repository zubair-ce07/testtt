import React, {Component} from 'react';
import {connect} from 'react-redux';


class ProfilePage extends Component {
    componentWillMount() {
        if (!this.props.isAuthenticated) this.props.history.push('/login/');
        this.user_id = this.props.match.params.user_id;
    }

    render() {
        return <div className="page-content">Profile Page : {this.user_id}</div>;
    }
}

function mapStateToProps({auth_user: {isAuthenticated, user}}) {
    return {isAuthenticated, user};
}

export default connect(mapStateToProps)(ProfilePage);
