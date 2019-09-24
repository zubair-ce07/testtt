import React from 'react';
import Popover from '@material-ui/core/Popover';
import {Button, CircularProgress, Container, Dialog, List, ListItem, Typography, withStyles} from "@material-ui/core";
import axios from 'axios'

const styles = theme => ({
    typography: {
        padding: theme.spacing(2),
    },
});

class NotificationPanel extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'anchorEl': null,
            'notifications': []
        };
    }

    fetchNotifications = () => {
        axios.get('http://localhost:8000/api/users/6/notifications/')
            .then(response => {
                this.setState({
                    'notifications': response.data
                });
            })
    };

    handleClick = event => {
        this.fetchNotifications();
        this.setState({
            'anchorEl': event.currentTarget
        });
    };

    handleClose = () => {
        this.setState({
            'anchorEl': null
        });
    };

    handleNotificationView = event => {

    }

    render() {
        const {classes} = this.props;
        const open = Boolean(this.state.anchorEl);
        const id = open ? 'simple-popover' : undefined;

        return (
            <div>
                <Popover
                    id={id}
                    open={open}
                    anchorEl={this.state.anchorEl}
                    onClose={this.handleClose}
                    anchorOrigin={{
                        vertical: 'bottom',
                        horizontal: 'center',
                    }}
                    transformOrigin={{
                        vertical: 'top',
                        horizontal: 'center',
                    }}
                >
                    <List>
                        {
                            this.state.notifications == null ?
                                <CircularProgress/> :
                                this.state.notifications.length > 0 ?
                                    this.state.notifications.map((notification, index) => {
                                        return (
                                            <ListItem key={index}>
                                                <Container>
                                                    <Typography>
                                                        {notification.text}
                                                    </Typography>
                                                    <Button onClick={this.handleNotificationView}>
                                                        View
                                                    </Button>
                                                    <Dialog>

                                                    </Dialog>
                                                </Container>

                                                <Typography>
                                                    {notification.created_at}
                                                </Typography>
                                            </ListItem>
                                        );
                                    }) :
                                    <ListItem>
                                        <Typography>
                                            No notifications
                                        </Typography>
                                    </ListItem>
                        }
                    </List>
                </Popover>
            </div>
        );
    }
}

export default withStyles(styles)(NotificationPanel);