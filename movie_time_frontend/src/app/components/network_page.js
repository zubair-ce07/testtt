import React, {Component} from 'react';
import {connect} from "react-redux";
import Waypoint from 'react-waypoint';

import {UserList} from './user_list';
import {fetchMore} from '../actions/more_content_actions';
import {setActivePage} from '../actions/active_page_actions';
import {fetchNetwork} from '../actions/user_actions';
import {FOLLOWED_BY, FOLLOWS} from "../utils/page_types";


class NetworkPage extends Component {
    componentWillMount() {
        if (!this.props.isAuthenticated) this.props.history.push('/login/');
        this.updateContentAndSetActivePage();
    }

    componentDidUpdate(prevProps) {
        if (this.props.match.params.type !== prevProps.match.params.type) {
            this.updateContentAndSetActivePage();
        }
    }

    updateContentAndSetActivePage() {
        const {type} = this.props.match.params;
        if (type === "follows") {
            this.props.fetchNetwork('follows');
            this.props.setActivePage(FOLLOWS);
        }
        if (type === "followings") {
            this.props.fetchNetwork('followed-by');
            this.props.setActivePage(FOLLOWED_BY);
        }
    }

    loadMore() {
        if (this.props.user_network.next !== null)
            this.props.fetchMore(this.props.user_network.next);
    }

    render() {
        return <div className="page-content row">
            <div className="col-md-3"/>
            <div className="col-md-6">
                {!this.props.user_network.isFetching && this.props.user_network.users.length === 0 &&
                <h4 className="text-center my-5">Your Network seems to be Empty!</h4>}
                <UserList users={this.props.user_network.users}/>
                {this.props.user_network.isFetching ? <h4 className="text-center my-5">Loading...</h4>
                    : <Waypoint onEnter={() => this.loadMore()} bottomOffset="-100%"/>}
            </div>
        </div>
    }
}

function mapStateToProps({auth_user: {isAuthenticated}, user_network}) {
    return {isAuthenticated, user_network};
}

export default connect(mapStateToProps, {
    fetchNetwork,
    setActivePage,
    fetchMore
})(NetworkPage);
