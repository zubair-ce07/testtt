import React, { Component } from 'react';
import { connect } from 'react-redux';
import Chart from './chart';
import GoogleMaps from './google_maps';


class WeatherList extends Component {
    renderWeather(cityData) {
        if(!cityData) {
            return
        }

        const name = cityData.city.name;
        const temps = cityData.list.map(weather => weather.main.temp);
        const humidities = cityData.list.map(weather => weather.main.humidity);
        const pressures = cityData.list.map(weather => weather.main.pressure);
        const { lon, lat } = cityData.city.coord;

        return (
            <tr key={name}>
                <td><GoogleMaps lon={lon} lat={lat} /></td>
                <td>
                    <Chart height={120} width={170} data={temps} color='red' units='Celsius' />
                </td>
                <td>
                    <Chart height={120} width={170} data={humidities} color='blue' units='%' />
                </td>
                <td>
                    <Chart height={120} width={170} data={pressures} color='green' units='hPa' />
                </td>
            </tr>
        );
    }

    render() {
        return (
            <table className='table table-hover'>
                <thead>
                    <tr>
                        <th>City</th>
                        <th>Temparature (Celsius)</th>
                        <th>Humidity (%)</th>
                        <th>Pressure (hPa)</th>
                    </tr>
                </thead>
                <tbody>
                    {this.props.weather.map(this.renderWeather)}
                </tbody>
            </table>
        );
    }
}

function mapStateToProps({ weather }) {
    return { weather };
}

export default connect(mapStateToProps)(WeatherList);
