import React from 'react';
import {List, ListItem, ListItemIcon, ListItemText} from '@material-ui/core';
import HomeIcon from '@material-ui/icons/Home'
import PeopleIcon from '@material-ui/icons/Contacts'
import ProfileIcon from '@material-ui/icons/Person'
import GroupIcon from '@material-ui/icons/Group'
import MessagesIcon from '@material-ui/icons/Email'

export const drawer = (
    <div>
        <List>
            <ListItem button>
                <ListItemIcon><HomeIcon/></ListItemIcon>
                <ListItemText primary={'Home'}/>
            </ListItem>
            <ListItem button>
                <ListItemIcon><PeopleIcon/></ListItemIcon>
                <ListItemText primary={'People'}/>
            </ListItem>
            <ListItem button>
                <ListItemIcon><GroupIcon/></ListItemIcon>
                <ListItemText primary={'Groups'}/>
            </ListItem>
            <ListItem button>
                <ListItemIcon><ProfileIcon/></ListItemIcon>
                <ListItemText primary={'Profile'}/>
            </ListItem>
            <ListItem button>
                <ListItemIcon><MessagesIcon/></ListItemIcon>
                <ListItemText primary={'Messages'}/>
            </ListItem>
        </List>
    </div>
);
