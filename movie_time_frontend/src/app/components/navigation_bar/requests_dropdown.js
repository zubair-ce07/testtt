import _ from 'lodash';
import {connect} from 'react-redux';
import React, {Component} from 'react';
import {NavDropdown, DropdownToggle, DropdownMenu} from 'reactstrap';

import FollowRequest from './follow_request_item';
import {respondToFollowRequest} from '../../actions/notification_actions';


class RequestsDropDown extends Component {
    constructor(props) {
        super(props);

        this.toggle = this.toggle.bind(this);
        this.state = {
            isOpen: false
        };
    }

    toggle() {
        this.setState({
            isOpen: !this.state.isOpen
        });
    }

    renderNotifications() {
        return _.map(this.props.user_requests, follow_request => {
            return <FollowRequest follow_request={follow_request} key={follow_request.id}
                                  onAccept={requestId => this.props.respondToFollowRequest(requestId, 'accept')}
                                  onBlock={requestId => this.props.respondToFollowRequest(requestId, 'block')}/>
        });
    }

    render() {
        const {user_requests} = this.props;
        let no_request_message = null;
        if (_.isEmpty(user_requests))
            no_request_message = <div className="no-notification-item">Huh! No one wants to follow ya!</div>;

        return (
            <NavDropdown isOpen={this.state.isOpen} toggle={this.toggle}>
                <DropdownToggle nav><i className="fa fa-group"/></DropdownToggle>
                <DropdownMenu right>
                    {no_request_message === null ? this.renderNotifications() : no_request_message}
                </DropdownMenu>
            </NavDropdown>
        );
    }
}

function mapStateToProps({notifications: {user_requests}}) {
    return {user_requests};
}

export default connect(mapStateToProps, {respondToFollowRequest})(RequestsDropDown);
