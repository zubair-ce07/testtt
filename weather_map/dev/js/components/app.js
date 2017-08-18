import React from 'react';
import { Grid } from 'react-bootstrap';

import SearchBar from '../containers/search_bar';
import WeatherList from './weather_data_list'
import { connect } from "react-redux";


class App extends React.Component
{
    displayError()
    {
        if(this.props.error)
        {
            return (
                <div className="alert alert-danger">
                    <strong>Weather Data not found</strong>
                </div>
            )
        }
    }

    render()
    {
        return (
            <div>
                <Grid>
                    <SearchBar/>
                    { this.displayError() }
                    <WeatherList/>
                </Grid>
            </div>
        )
    }
}

function mapStateToProps(state)
{
    return {
        error: state.weather.error
    }
}

export default connect(mapStateToProps)(App);