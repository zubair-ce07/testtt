import React from 'react';
import PropTypes from "prop-types";
import {withStyles} from '@material-ui/core/styles';
import ListSubheader from '@material-ui/core/ListSubheader';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import Collapse from '@material-ui/core/Collapse';
import SchoolIcon from '@material-ui/icons/School';
import GroupIcon from '@material-ui/icons/Group';
import WorkIcon from '@material-ui/icons/Work';
import ExpandLess from '@material-ui/icons/ExpandLess';
import ExpandMore from '@material-ui/icons/ExpandMore';
import FriendIcon from '@material-ui/icons/EmojiPeople';
import {Card, Typography} from "@material-ui/core";
import CardContent from "@material-ui/core/CardContent";
import {AcademicInformationAPI, FriendListAPI, GroupDataAPI, WorkInformationAPI} from "../../APIClient/APIClient";

const styles = theme => ({
    root: {
        width: '100%',
        maxWidth: 400,
        backgroundColor: theme.palette.background.paper,
    },
    nested: {
        paddingLeft: theme.spacing(6),
    },
});

class SideInformationBar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            Groups: false,
            WorkInformations: false,
            AcademicInformations: false,
            Friends: false,
            groups: [],
            work_informations: [],
            academic_informations: [],
            friends: [],
        }
    }

    handleClickGroup = () => {
        this.setState({Groups: !this.state.Groups});
    };

    handleClickAcademicInformation = () => {
        this.setState({AcademicInformations: !this.state.AcademicInformations});
    };

    handleClickWorkInformation = () => {
        this.setState({WorkInformations: !this.state.WorkInformations});
    };

    handleClickFriend = () => {
        this.setState({Friends: !this.state.Friends});
    };

    fetchGroupData = () => {
        GroupDataAPI()
            .then(response => {
                this.setState({
                    groups: response.data
                });
            })
    };
    fetchWorkInformationData = link => {
        WorkInformationAPI(link)
            .then(response => {
                this.setState({
                    work_informations: response.data
                });
            });
    };
    fetchAcademicInformationData = link => {
        AcademicInformationAPI(link)
            .then(response => {
                this.setState({
                    academic_informations: response.data
                });
            })
    };
    fetchFriendListData = () => {
        FriendListAPI()
            .then(response => {
                this.setState({
                    friends: response.data
                });
            })
    };

    componentDidMount() {
        this.fetchGroupData();
        this.fetchFriendListData();
        this.fetchWorkInformationData(this.props.links['work_information_url']);
        this.fetchAcademicInformationData(this.props.links['academic_information_url']);
    }

    render() {
        const {classes} = this.props;
        return (
            <Card
                className={classes.root}>
                <CardContent>
                    <List
                        component="nav"
                        aria-labelledby="nested-list-subheader"
                        subheader={
                            <ListSubheader component="div" id="nested-list-subheader">
                                Other Information
                            </ListSubheader>
                        }
                    >
                        <ListItem button onClick={this.handleClickGroup}>
                            <ListItemIcon>
                                <GroupIcon/>
                            </ListItemIcon>
                            <ListItemText primary="Groups"/>
                            {this.state.Groups ? <ExpandLess/> : <ExpandMore/>}
                        </ListItem>
                        <Collapse in={this.state.Groups} timeout="auto" unmountOnExit>
                            <List component="div" disablePadding>
                                {
                                    this.state.groups.length > 0 ?
                                        this.state.groups.map((data, index) => {
                                            return (
                                                <ListItem key={index} button className={classes.nested}>
                                                    <ListItemText primary={data.name}/>
                                                </ListItem>
                                            );
                                        }) :
                                        <ListItem className={classes.nested}>
                                            <Typography variant="overline">
                                                No groups joined
                                            </Typography>
                                        </ListItem>
                                }
                            </List>
                        </Collapse>

                        <ListItem button onClick={this.handleClickFriend}>
                            <ListItemIcon>
                                <FriendIcon/>
                            </ListItemIcon>
                            <ListItemText primary="Friends"/>
                            {this.state.Friends ? <ExpandLess/> : <ExpandMore/>}
                        </ListItem>
                        <Collapse in={this.state.Friends} timeout="auto" unmountOnExit>
                            <List component="div" disablePadding>
                                {
                                    this.state.friends.length > 0 ?
                                        this.state.friends.map((data, index) => {
                                            return (
                                                <ListItem key={index} button className={classes.nested}>
                                                    <ListItemText primary={data.first_name + ' ' + data.last_name}/>
                                                </ListItem>
                                            );
                                        }) :
                                        <ListItem className={classes.nested}>
                                            <Typography variant="overline">
                                                No friends
                                            </Typography>
                                        </ListItem>
                                }
                            </List>
                        </Collapse>
                        <ListItem button onClick={this.handleClickWorkInformation}>
                            <ListItemIcon>
                                <WorkIcon/>
                            </ListItemIcon>
                            <ListItemText primary="Work Information"/>
                            {this.state.WorkInformations ? <ExpandLess/> : <ExpandMore/>}
                        </ListItem>
                        <Collapse in={this.state.WorkInformations} timeout="auto" unmountOnExit>
                            <List component="div" disablePadding>
                                {
                                    this.state.work_informations.length > 0 ?
                                        this.state.work_informations.map((data, index) => {
                                            return (
                                                <ListItem key={index} button className={classes.nested}>
                                                    <ListItemText primary={data.job_title}/>
                                                </ListItem>
                                            );
                                        }) :
                                        <ListItem className={classes.nested}>
                                            <Typography variant="overline">
                                                No work records
                                            </Typography>
                                        </ListItem>
                                }
                            </List>
                        </Collapse>
                        <ListItem button onClick={this.handleClickAcademicInformation}>
                            <ListItemIcon>
                                <SchoolIcon/>
                            </ListItemIcon>
                            <ListItemText primary="Academic Information"/>
                            {this.state.AcademicInformations ? <ExpandLess/> : <ExpandMore/>}
                        </ListItem>
                        <Collapse in={this.state.AcademicInformations} timeout="auto" unmountOnExit>
                            <List component="div" disablePadding>
                                {
                                    this.state.academic_informations.length > 0 ?
                                        this.state.academic_informations.map((data, index) => {
                                            return (
                                                <ListItem key={index} button className={classes.nested}>
                                                    <ListItemText primary={data.institution_name}/>
                                                </ListItem>
                                            );
                                        }) :
                                        <ListItem className={classes.nested}>
                                            <Typography variant="overline">
                                                No academic records
                                            </Typography>
                                        </ListItem>
                                }
                            </List>
                        </Collapse>
                    </List>
                </CardContent>
            </Card>
        );
    }
}

SideInformationBar.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(SideInformationBar);
