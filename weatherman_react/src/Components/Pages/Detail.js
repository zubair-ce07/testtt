import React from "react"
import {Typography, Paper, GridList, GridListTile} from "@material-ui/core/"
import axios from "axios";
import * as constants from '../../constants'

import MonthCard from '../Partials/MonthCard'
import SimpleSelect from '../Partials/SimpleSelect'


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

export default class Detail extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            cityId: props.match.params.cityId,
            cityName: props.match.params.cityName,
            years: null,
            yearlyWeather: null,
            monthlyWeather: null
        }
    }

    componentDidMount() {
        document.title="Weather Detail of "+this.state.cityName+" - Weatherman";
        var cityId = this.state.cityId;
        var self = this;

        axios.get(constants.BASE_URL + 'weather/years/' + cityId)
            .then(function (response) {
                self.setState({years: response.data})

            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })


    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        var cityId = this.props.match.params.cityId;
        var self = this;
        if (cityId !== prevState.cityId) {
            document.title="Weather Detail of "+this.props.match.params.cityName+" - Weatherman";
            selectedYear = "";
            this.setState({
                cityId: cityId,
                cityName: this.props.match.params.cityName,
                years: null,
                yearlyWeather: null,
                monthlyWeather: null
            })
            axios.get(constants.BASE_URL + 'weather/years/' + cityId)
                .then(function (response) {
                    self.setState({years: response.data})

                })
                .catch(function (error) {
                    // handle error
                    console.log(error);
                })
        }

    }

    componentWillUnmount() {
        selectedYear = "";
    }

    handleSelect(e) {
        var year = e.target.value;
        // if it would be a state, when i save the state here, it would call render again which is useless
        selectedYear = year;
        var self = this;
        axios.get(constants.BASE_URL + 'weather/average-monthly/' + year)
            .then(function (response) {
                self.setState({monthlyWeather: response.data})

            })
            .catch(function (error) {
                // handle error
                console.error(error);
            });
        axios.get(constants.BASE_URL + 'weather/yearly/' + year)
            .then(function (response) {
                self.setState({yearlyWeather: response.data})

            })
            .catch(function (error) {
                // handle error
                console.log(error);
            });
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
                {this.state.years &&

                <div>
                    {this.state.years.length > 0 &&

                    <div>
                        <Paper className="paper-style">
                            <SimpleSelect handleSelect={this.handleSelect.bind(this)}
                                          label={"Select Year"}
                                          selected={selectedYear}
                                          items={this.state.years}/>
                        </Paper>
                        {this.state.yearlyWeather &&
                        <Paper className="paper-style">
                            <h3>Yearly Weather of {this.state.cityName} of year {selectedYear}</h3>
                            <Typography variant="subheading">
                                Higest: <span>{this.state.yearlyWeather.higest_temperature}&deg;C</span>
                                <br/>
                                Lowest: <span>{this.state.yearlyWeather.lowest_temperature}&deg;C</span>
                                <br/>
                                Most Humid: <span>{this.state.yearlyWeather.humidity}</span>%<br/>
                            </Typography>
                        </Paper>
                        }
                        {this.state.monthlyWeather &&
                        <Paper className="paper-style">
                            <div className={classes.root}>
                                <GridList cellHeight={180} cols={3} className={classes.gridList}>
                                    <GridListTile key="Subheader" cols={3} style={{height: 'auto'}}>
                                        <h3>Monthly Weather of {this.state.cityName} of
                                            year {selectedYear}</h3>
                                    </GridListTile>
                                    {this.state.monthlyWeather.map((monthly, index) =>
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
                    {this.state.years.length === 0 &&
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