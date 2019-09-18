import React from 'react';
import PropTypes from 'prop-types';
import AppBar from '@material-ui/core/AppBar';
import CssBaseline from '@material-ui/core/CssBaseline';
import Drawer from '@material-ui/core/Drawer';
import Hidden from '@material-ui/core/Hidden';
import IconButton from '@material-ui/core/IconButton';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import MenuIcon from '@material-ui/icons/Menu';
import HomeIcon from '@material-ui/icons/Home'
import PeopleIcon from '@material-ui/icons/Contacts'
import ProfileIcon from '@material-ui/icons/Person'
import GroupIcon from '@material-ui/icons/Group'
import MessagesIcon from '@material-ui/icons/Email'
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import {makeStyles, useTheme} from '@material-ui/core/styles';

const drawerWidth = 300;

const useStyles = makeStyles(theme => ({
    root: {
        display: 'flex',
    },
    drawer: {
        [theme.breakpoints.up('sm')]: {
            width: drawerWidth,
            flexShrink: 0,
        },
    },
    appBar: {
        backgroundColor: '#4AA8E0',
    },
    menuButton: {
        marginRight: theme.spacing(2),
        [theme.breakpoints.up('sm')]: {
            display: 'none',
        },
    },
    toolbar: theme.mixins.toolbar,
    drawerPaper: {
        width: drawerWidth,
        marginTop: theme.spacing(8),
    },
    drawerPaperMobile: {
        width: drawerWidth,
    },
    content: {
        flexGrow: 1,
        padding: theme.spacing(3),
    },
    avatar: {
        transform: 'scale(0.75, 0.75)',
    }
}));

function AppSidebar(props) {
    const {container} = props;
    const classes = useStyles();
    const theme = useTheme();
    const [mobileOpen, setMobileOpen] = React.useState(false);

    function handleDrawerToggle() {
        setMobileOpen(!mobileOpen);
    }

    const drawer = (
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
                    <ListItemIcon><ProfileIcon /></ListItemIcon>
                    <ListItemText primary={'Profile'}/>
                </ListItem>
                <ListItem button>
                    <ListItemIcon><MessagesIcon/></ListItemIcon>
                    <ListItemText primary={'Messages'}/>
                </ListItem>
            </List>
        </div>
    );

    return (
        <div className={classes.root}>
            <CssBaseline/>
            <AppBar position="fixed" className={classes.appBar}>
                <Toolbar>
                    <IconButton
                        color="inherit"
                        aria-label="open drawer"
                        edge="start"
                        onClick={handleDrawerToggle}
                        className={classes.menuButton}
                    >
                        <MenuIcon/>
                    </IconButton>
                    <Typography variant="h6" noWrap>
                        Social App
                    </Typography>
                </Toolbar>
            </AppBar>
            <nav className={classes.drawer} aria-label="mailbox folders">
                <Hidden smUp implementation="css">
                    <Drawer
                        container={container}
                        variant="temporary"
                        anchor={theme.direction === 'rtl' ? 'right' : 'left'}
                        open={mobileOpen}
                        onClose={handleDrawerToggle}
                        classes={{
                            paper: classes.drawerPaperMobile,
                        }}
                        ModalProps={{
                            keepMounted: true, // Better open performance on mobile.
                        }}
                    >
                        {drawer}
                    </Drawer>
                </Hidden>
                <Hidden xsDown implementation="css">
                    <Drawer
                        classes={{
                            paper: classes.drawerPaper,
                        }}
                        variant="permanent"
                        open
                    >
                        {drawer}
                    </Drawer>
                </Hidden>
            </nav>
        </div>
    );
}

AppSidebar.propTypes = {
    container: PropTypes.instanceOf(typeof Element === 'undefined' ? Object : Element),
};

export default AppSidebar;
