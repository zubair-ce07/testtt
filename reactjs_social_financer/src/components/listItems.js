import React from 'react';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';
import DashboardIcon from '@material-ui/icons/Dashboard';
import PeopleIcon from '@material-ui/icons/People';
import PersonIcon from '@material-ui/icons/Person';
import { Link } from "react-router-dom";
import AssignmentIcon from '@material-ui/icons/Assignment';

export const mainListDonorItems = (
  <div>
    <Link to="/unpaired-consumers">
      <ListItem button  >
        <ListItemIcon>
          <DashboardIcon />
        </ListItemIcon>
        <ListItemText primary="Select Consumers" />
      </ListItem>
    </Link>

    <Link to="/paired-consumers">
    <ListItem button  >
      <ListItemIcon>
        <PeopleIcon />
      </ListItemIcon>
      <ListItemText primary="My Consumers" />
    </ListItem>
    </Link>

    <Link to="/my-profile">
    <ListItem button  >
      <ListItemIcon>
        <PersonIcon />
      </ListItemIcon>
      <ListItemText primary="My Profile" />
    </ListItem>
    </Link>
  </div>
);

export const mainListConsumerItems = (
  <div>
    <Link to="/my-donor">
    <ListItem button>
      <ListItemIcon>
        <PeopleIcon />
      </ListItemIcon>
      <ListItemText primary="My Donor" />
    </ListItem>
    </Link>

    <Link to="/my-profile">
    <ListItem button>
      <ListItemIcon>
        <PersonIcon />
      </ListItemIcon>
      <ListItemText primary="My Profile" />
    </ListItem>
    </Link>
  </div>
);


export const secondaryListItems = (
  <div>
    <Link to="/">
    <ListSubheader inset>Options</ListSubheader>
    <ListItem button>
      <ListItemIcon>
        <AssignmentIcon />
      </ListItemIcon>
      <ListItemText primary="Sign out" />
    </ListItem>
    </Link>

  </div>
);
