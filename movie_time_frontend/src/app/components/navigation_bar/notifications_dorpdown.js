import _ from 'lodash';
import React, {Component} from 'react';
import {connect} from 'react-redux';
import {NavDropdown, DropdownToggle, DropdownMenu} from 'reactstrap'

import Notification from './notification_item';
import {fetchNotifications, deleteNotification} from '../../actions/notification_actions';


class NotificationDropDown extends Component {
    constructor(props) {
        super(props);

        this.toggle = this.toggle.bind(this);
        this.state = {
            isOpen: false
        };
    }

    componentWillMount() {
        this.props.fetchNotifications()
    }

    toggle() {
        this.setState({
            isOpen: !this.state.isOpen
        });
    }

    renderNotifications() {

        return _.map(this.props.moviesReleased, notification => {
            return <Notification notification={notification} key={notification.id}
                                 onDelete={(notification_id) => this.props.deleteNotification(notification_id)}/>
        });
    }

    render() {
        const {moviesReleased} = this.props;
        let no_notification_message = null;
        if (_.isEmpty(moviesReleased))
            no_notification_message = <div className="no-notification-item">Hurray! You are all caught up.</div>;

        return (
            <NavDropdown isOpen={this.state.isOpen} toggle={this.toggle}>
                <DropdownToggle nav><i className="fa fa-bell"/></DropdownToggle>
                <DropdownMenu right>
                    {no_notification_message === null ? this.renderNotifications() : no_notification_message}
                </DropdownMenu>
            </NavDropdown>
        );
    }

}

function mapStateToProps({notifications: {moviesReleased}}) {
    return {moviesReleased};
}

export default connect(mapStateToProps, {fetchNotifications, deleteNotification})(NotificationDropDown);
