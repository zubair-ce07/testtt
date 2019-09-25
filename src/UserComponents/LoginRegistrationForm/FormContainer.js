import React from 'react';
import PropTypes from 'prop-types';
import SwipeableViews from 'react-swipeable-views';
import {makeStyles, useTheme} from '@material-ui/core/styles';
import {AppBar, Box, Tab, Tabs, Typography} from '@material-ui/core';

import RegistrationForm from './RegistrationForm'
import LoginForm from './LoginForm'

const TabPanel = props => {
    const {children, value, index, ...other} = props;
    return (
        <Typography
            component="div"
            role="tabpanel" 
            hidden={value !== index}
            id={`full-width-tabpanel-${index}`}
            aria-labelledby={`full-width-tab-${index}`}
            {...other}
        >
            <Box p={2}>{children}</Box>
        </Typography>
    );
};

TabPanel.propTypes = {
    children: PropTypes.node,
    index: PropTypes.any.isRequired,
    value: PropTypes.any.isRequired,
};

const useStyles = makeStyles(theme => ({
    root: {
        backgroundColor: theme.palette.background.paper,
        width: 500,
        margin: theme.spacing(4),
        alignItems: 'center',
    },
}));

const UserLoginRegistrationForm = () => {
    const classes = useStyles();
    const theme = useTheme();
    const [value, setValue] = React.useState(0);

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    const handleChangeIndex = index => {
        setValue(index);
    };

    return (
        <Box className={classes.root}>
            <AppBar position="static" color="default">
                <Tabs
                    value={value}
                    onChange={handleChange}
                    indicatorColor="primary"
                    textColor="primary"
                    variant="fullWidth"
                >
                    <Tab label="Login"  />
                    <Tab label="Register" />
                </Tabs>
            </AppBar>

            <SwipeableViews
                axis={theme.direction === 'rtl' ? 'x-reverse' : 'x'}
                index={value}
                onChangeIndex={handleChangeIndex}
            >
                <TabPanel value={value} index={0} dir={theme.direction}>
                    <LoginForm/>
                </TabPanel>
                <TabPanel value={value} index={1} dir={theme.direction}>
                    <RegistrationForm/>
                </TabPanel>
            </SwipeableViews>
        </Box>
    );
};

export default UserLoginRegistrationForm;
