import React from 'react';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import Avatar from '@material-ui/core/Avatar';
import {red} from '@material-ui/core/colors';
import AddressIcon from '@material-ui/icons/Room';
import DraftsIcon from '@material-ui/icons/Drafts';
import PhoneIcon from '@material-ui/icons/LocalPhone';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import withStyles from "@material-ui/core/styles/withStyles";
import PropTypes from "prop-types";

const styles = theme => ({
    card: {
        position: 'absolute',
        width: 1200,
    },
    media: {
        height: 100,
    },
    expand: {
        transform: 'rotate(0deg)',
        marginLeft: 'auto',
        transition: theme.transitions.create('transform', {
            duration: theme.transitions.duration.shortest,
        }),
    },
    expandOpen: {
        transform: 'rotate(180deg)',
    },
    avatar: {
        backgroundColor: red[500],
        transform: 'scale(1, 1)'
    },
});

class profileHeader extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'open': false,
        }
    }

    handleClick = () => {
        this.setState({'open': !this.state.open});
    };

    formatDate = date => {
        const options = {year: 'numeric', month: 'long', day: 'numeric'};
        return 'Born: ' + date.toLocaleDateString('en-US', options);
    };

    header = (name, classes) => {
        return (
            <CardHeader
                avatar={
                    <Avatar aria-label="recipe" className={classes.avatar}>
                        {name[0]}
                    </Avatar>
                }

                title={name}
                subheader={this.formatDate(new Date(this.props.profileInfo.date_of_birth))}
            />
        )
    };

    render() {
        const {classes} = this.props;
        return (
            <Card className={classes.card}>
                {
                    this.header(this.props.profileInfo.first_name + ' ' + this.props.profileInfo.last_name, classes)
                }

                <List
                    component="nav"
                    aria-labelledby="nested-list-subheader"
                    className={classes.root}
                >
                    <ListItem>
                        <ListItemIcon>
                            <PhoneIcon/>
                        </ListItemIcon>
                        <ListItemText primary={this.props.profileInfo.phone}/>
                    </ListItem>
                    <ListItem>
                        <ListItemIcon>
                            <DraftsIcon/>
                        </ListItemIcon>
                        <ListItemText primary={this.props.profileInfo.email}/>
                    </ListItem>
                    <ListItem>
                        <ListItemIcon>
                            <AddressIcon/>
                        </ListItemIcon>
                        <ListItemText primary={this.props.profileInfo.address}/>
                    </ListItem>
                </List>
            </Card>
        );
    }
}

profileHeader.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(profileHeader);