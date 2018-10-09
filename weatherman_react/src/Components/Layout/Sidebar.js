import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import ListSubheader from '@material-ui/core/ListSubheader';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import Collapse from '@material-ui/core/Collapse';
import KeyboardArrowRight from '@material-ui/icons/KeyboardArrowRight';
import LocationCity from '@material-ui/icons/LocationCity';
import ExpandLess from '@material-ui/icons/ExpandLess';
import ExpandMore from '@material-ui/icons/ExpandMore';
import Divider from '@material-ui/core/Divider';
import {connect} from 'react-redux';
import { Link } from 'react-router-dom'

import store from '../../store'


const styles = theme => ({
    root: {
        backgroundColor: "#F5F5F5",
        height: '100%'
    },
    nested: {
        paddingLeft: theme.spacing.unit * 4,
    },
});

const action = type => store.dispatch({type})

class Sidebar extends React.Component {
    constructor() {
        super();
        this.state = {
            cityOpen: true,
            yearOpen: false,
        }
    }

    componentDidMount() {
        action('FETCH_CITIES')
    }

    handleCityMenuClick = () => {
        this.setState(state => ({cityOpen: !state.cityOpen}));
    };

    render() {
        const {classes} = this.props;
        return (
            <div className={classes.root}>

                <List
                    component="nav"
                    subheader={<ListSubheader component="div">Filter Weather By
                        City</ListSubheader>}
                >
                    <Divider/>
                    <ListItem button onClick={this.handleCityMenuClick}>
                        <ListItemIcon>
                            <LocationCity/>
                        </ListItemIcon>
                        <ListItemText inset primary="Cities"/>
                        {this.state.cityOpen ? <ExpandLess/> : <ExpandMore/>}
                    </ListItem>

                    {this.props.cities &&
                    <Collapse in={this.state.cityOpen} timeout="auto" unmountOnExit>
                        <List component="div" disablePadding>
                            {this.props.cities.map((city) =>

                                <Link className="link-style" key={city.id} to={'/city/'+city.id+'/'+city.name}>
                                <ListItem  className={classes.nested}>
                                    <ListItemIcon>
                                        <KeyboardArrowRight/>
                                    </ListItemIcon>
                                    <ListItemText inset primary={city.name}/>
                                </ListItem>
                                </Link>
                            )}
                        </List>
                    </Collapse>
                    }
                </List>
                <Divider/>



            </div>
        );
    }
}

Sidebar.propTypes = {
    classes: PropTypes.object.isRequired,
};


function mapStateToProps(state) {
    return {
        cities: state.cities
    };
}



export default connect(mapStateToProps)(withStyles(styles)(Sidebar));
