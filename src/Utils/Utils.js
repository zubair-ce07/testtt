import React from 'react';
import {List, ListItem, ListItemIcon, ListItemText} from '@material-ui/core'
import HomeIcon from '@material-ui/icons/Home'
import PeopleIcon from '@material-ui/icons/Contacts'
import GroupIcon from '@material-ui/icons/Group'
import MessagesIcon from '@material-ui/icons/Email'
import Typography from "@material-ui/core/Typography";
import {Link} from "react-router-dom";

export const formatDate = date => {
    const options = {year: 'numeric', month: 'long', day: 'numeric'};
    return date.toLocaleDateString('en-US', options);
};

export const drawer = (
    <div>
        <List>
            <Link to='/home/'>
                <ListItem button>
                    <ListItemIcon><HomeIcon/></ListItemIcon>
                    <ListItemText primary={'Home'}/>
                </ListItem>
            </Link>
            <ListItem button>
                <ListItemIcon><PeopleIcon/></ListItemIcon>
                <ListItemText primary={'People'}/>
            </ListItem>
            <ListItem button>
                <ListItemIcon><GroupIcon/></ListItemIcon>
                <ListItemText primary={'Groups'}/>
            </ListItem>
            <Link to='/profile/'>
                <ListItem button>
                    <ListItemIcon><HomeIcon/></ListItemIcon>
                    <ListItemText primary={'Profile'}/>
                </ListItem>
            </Link>
            <ListItem button>
                <ListItemIcon><MessagesIcon/></ListItemIcon>
                <ListItemText primary={'Messages'}/>
            </ListItem>
        </List>
    </div>
);

export const Copyright = () => {
    return (
        <Typography variant="body2" color="textSecondary" align="center">
            {'Copyright © '}
            Social App
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    );
};

