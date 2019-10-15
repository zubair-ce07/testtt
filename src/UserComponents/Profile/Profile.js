import React from 'react';
import PropTypes from 'prop-types';
import {CircularProgress} from '@material-ui/core';
import withStyles from '@material-ui/core/styles/withStyles';
import SideInformationBar from './SideInformationBar';
import ProfileHeader from './profileHeader'
import NewPost from '../../PostComponents/NewPost/NewPost';
import {UserProfileAPI} from '../../APIClient/APIClient';

const styles = theme => ({
    header: {
        overflow: 'auto',
        marginLeft: theme.spacing(20),
        marginTop: theme.spacing(10)
    },
    sidebar: {
        marginLeft: theme.spacing(20),
        marginTop: theme.spacing(32),
        display: 'inline-block'
    },
    newpost: {
        marginLeft: theme.spacing(20),
        marginTop: theme.spacing(32),
        float: 'right',
    }
});

class Profile extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            userprofile: null,
            links: null
        }
    }

    getUserData = () => {
        UserProfileAPI()
            .then(response => {
                let links = {
                    'academic_information_url': response.data['academic_information_url'],
                    'work_information_url': response.data['work_information_url']
                };
                delete response.data['academic_information_url'];
                delete response.data['work_information_url'];

                this.setState({
                    userprofile: response.data,
                    links: links
                });
            })
    };

    componentDidMount() {
        this.getUserData()
    }

    render() {
        const {classes} = this.props;
        return (
            <div>
                <div className={classes.header}>
                    {
                        this.state.userprofile ?
                            <ProfileHeader profileInfo={this.state.userprofile}/> :
                            <CircularProgress/>
                    }
                </div>
                <div className={classes.sidebar}>
                    {
                        this.state.links ?
                            <SideInformationBar links={this.state.links}/> :
                            <CircularProgress/>
                    }
                </div>
                <div className={classes.newpost}>
                    <NewPost/>
                </div>
            </div>

        );
    }
}

Profile.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Profile);
