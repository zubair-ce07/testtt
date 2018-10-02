import React from "react"
import {Typography, Paper, GridList, GridListTile, Divider} from "@material-ui/core/"
import axios from "axios";
import * as constatnts from '../../constants'

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

let selectedYear="";

export default class Index extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            years: null,
            yearlyWeather: null,
            monthlyWeather: null

        }
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        var cityId = this.props.cityId;
        var self = this;
        if (cityId !== prevProps.cityId) {
            axios.get(constatnts.BASE_URL + 'weather/years/' + cityId)
                .then(function (response) {
                    self.setState({years: response.data})

                })
                .catch(function (error) {
                    // handle error
                    console.log(error);
                })
        }

    }

    handleSelect(e) {
        var year = e.target.value;
        selectedYear=year;
        var self = this;
        axios.get(constatnts.BASE_URL + 'weather/average-monthly/' + year)
            .then(function (response) {
                self.setState({monthlyWeather: response.data})

            })
            .catch(function (error) {
                // handle error
                console.log(error);
            });
        axios.get(constatnts.BASE_URL + 'weather/yearly/' + year)
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
                    {this.props.cityId === null &&
                    <h3>Please select a city form sidebar to get started</h3>
                    }
                    {this.props.cityId !== null &&
                    <h3>Weather Report of City {this.props.cityName}</h3>
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
                            <h3>Yearly Weather of {this.props.cityName} of year {selectedYear}</h3>
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
                                        <h3>Monthly Weather of {this.props.cityName} of year {selectedYear}</h3>
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