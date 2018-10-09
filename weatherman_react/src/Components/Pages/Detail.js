import React from "react"
import {Typography, Paper, GridList, GridListTile} from "@material-ui/core/"
import {connect} from 'react-redux';

import MonthCard from '../Partials/MonthCard'
import SimpleSelect from '../Partials/SimpleSelect'
import store from "../../store";


const styles = theme => ({
    root: {
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-around',
        overflow: 'hidden',
        backgroundColor: theme.palette.background.paper,
    },
    gridList: {
        width: 500,
        height: 450,
    },
    icon: {
        color: 'rgba(255, 255, 255, 0.54)',
    },
});

let selectedYear = "";
const action = (type, payload) => store.dispatch({type, payload});

class Detail extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            cityId: props.match.params.cityId,
            cityName: props.match.params.cityName,

            monthlyWeather: null
        }
    }

    componentDidMount() {
        document.title="Weather Detail of "+this.state.cityName+" - Weatherman";
        var cityId = this.state.cityId;
        action('FETCH_YEARS', cityId)




    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        var cityId = this.props.match.params.cityId;
        if (cityId !== prevState.cityId) {
            document.title="Weather Detail of "+this.props.match.params.cityName+" - Weatherman";
            selectedYear = "";
            this.setState({
                cityId: cityId,
                cityName: this.props.match.params.cityName,


                monthlyWeather: null
            });
            action('FETCH_YEARS', cityId)
        }

    }

    componentWillUnmount() {
        action('RESET_WEATHER', null);
        selectedYear = "";
    }

    handleSelect(e) {
        var year = e.target.value;
        // if it would be a state, when i save the state here, it would call render again which is useless
        selectedYear = year;
        action('FETCH_MONTHLY_WEATHER', year);
        action('FETCH_YEARLY_WEATHER', year);
    }


    render() {
        const classes = styles;
        return (
            <div>
                <Paper className="paper-style">
                    <h1>Welcome to Weatherman</h1>
                    {this.state.cityId === null &&
                    <h3>Please select a city form sidebar to get started</h3>
                    }
                    {this.state.cityId !== null &&
                    <h3>Weather Report of City {this.state.cityName}</h3>
                    }

                </Paper>
                {this.props.years &&

                <div>
                    {this.props.years.length > 0 &&

                    <div>
                        <Paper className="paper-style">
                            <SimpleSelect handleSelect={this.handleSelect.bind(this)}
                                          label={"Select Year"}
                                          selected={selectedYear}
                                          items={this.props.years}/>
                        </Paper>
                        {this.props.yearlyWeather &&
                        <Paper className="paper-style">
                            <h3>Yearly Weather of {this.state.cityName} of year {selectedYear}</h3>
                            <Typography variant="subheading">
                                Higest: <span>{this.props.yearlyWeather.higest_temperature}&deg;C</span>
                                <br/>
                                Lowest: <span>{this.props.yearlyWeather.lowest_temperature}&deg;C</span>
                                <br/>
                                Most Humid: <span>{this.props.yearlyWeather.humidity}</span>%<br/>
                            </Typography>
                        </Paper>
                        }
                        {this.props.monthlyWeather &&
                        <Paper className="paper-style">
                            <div className={classes.root}>
                                <GridList cellHeight={180} cols={3} className={classes.gridList}>
                                    <GridListTile key="Subheader" cols={3} style={{height: 'auto'}}>
                                        <h3>Monthly Weather of {this.state.cityName} of
                                            year {selectedYear}</h3>
                                    </GridListTile>
                                    {this.props.monthlyWeather.map((monthly, index) =>
                                        <GridListTile key={index} cols={1}>
                                            <MonthCard month={monthly}/>
                                        </GridListTile>
                                    )}
                                </GridList>
                            </div>
                        </Paper>
                        }
                    </div>
                    }
                    {this.props.years.length === 0 &&
                    <Paper className="paper-style">
                        <h3>No weather record found for this city</h3>
                    </Paper>
                    }


                </div>
                }
            </div>
        )
    }
}

function mapStateToProps(state) {
    return {
        years: state.years,
        monthlyWeather: state.monthlyWeather,
        yearlyWeather: state.yearlyWeather
    };
}


export default connect(mapStateToProps)(Detail);