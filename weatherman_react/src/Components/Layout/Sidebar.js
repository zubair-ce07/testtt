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
import DateRange from '@material-ui/icons/DateRange';
import ExpandLess from '@material-ui/icons/ExpandLess';
import ExpandMore from '@material-ui/icons/ExpandMore';
import CalendarToday from '@material-ui/icons/CalendarToday';
import Divider from '@material-ui/core/Divider';
import * as constatnts from '../../constants'
import axios from "axios";


const styles = theme => ({
    root: {
        backgroundColor: "#F5F5F5",
        height: '100%'
    },
    nested: {
        paddingLeft: theme.spacing.unit * 4,
    },
});

class Sidebar extends React.Component {
    constructor() {
        super();
        this.state = {
            cities: null,
            // years: null,
            cityOpen: true,
            yearOpen: false,
        }
    }

    componentDidMount() {
        var self = this
        axios.get(constatnts.BASE_URL + 'weather/cities/')
            .then(function (response) {
                self.setState({cities: response.data})
            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })


    }

    handleCityMenuClick = () => {
        this.setState(state => ({cityOpen: !state.cityOpen}));
    };

    handleYearClick = () => {
        this.setState(state => ({yearOpen: !state.yearOpen}));
    };

    handleCityItemClick = (cityId, cityName) =>{
        this.props.setCity(cityId, cityName)
    };

    handleYearItemClick = (year) =>{

        console.log(year)
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

                    {this.state.cities &&
                    <Collapse in={this.state.cityOpen} timeout="auto" unmountOnExit>
                        <List component="div" disablePadding>
                            {this.state.cities.map((city) =>


                                <ListItem key={city.id} button className={classes.nested} onClick={this.handleCityItemClick.bind(this, city.id, city.name)}>
                                    <ListItemIcon>
                                        <KeyboardArrowRight/>
                                    </ListItemIcon>
                                    <ListItemText inset primary={city.name}/>
                                </ListItem>
                            )}
                        </List>
                    </Collapse>
                    }
                </List>
                <Divider/>
                {/*<Divider/>*/}

                {/*<List*/}
                    {/*component="nav"*/}
                    {/*subheader={<ListSubheader component="div">Filter Weather By*/}
                        {/*Year</ListSubheader>}*/}
                {/*>*/}
                    {/*<Divider/>*/}
                    {/*<ListItem button onClick={this.handleYearClick}>*/}
                        {/*<ListItemIcon>*/}
                            {/*<DateRange/>*/}
                        {/*</ListItemIcon>*/}
                        {/*<ListItemText inset primary="Years"/>*/}
                        {/*{this.state.yearOpen ? <ExpandLess/> : <ExpandMore/>}*/}
                    {/*</ListItem>*/}
                    {/*{this.states.year &&*/}
                    {/*<Collapse in={this.state.yearOpen} timeout="auto" unmountOnExit>*/}
                        {/*<List component="div" disablePadding>*/}
                            {/*{this.state.years.map((year, index) =>*/}
                                {/*<ListItem key={index} button className={classes.nested} onClick={this.handleYearItemClick.bind(this, year.year)}>*/}
                                    {/*<ListItemIcon>*/}
                                        {/*<CalendarToday/>*/}
                                    {/*</ListItemIcon>*/}
                                    {/*<ListItemText inset primary={year.year}/>*/}
                                {/*</ListItem>*/}
                            {/*)}*/}
                        {/*</List>*/}
                    {/*</Collapse>*/}
                    {/*}*/}
                {/*</List>*/}


            </div>
        );
    }
}

Sidebar.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Sidebar);