import React, { Component } from 'react';
import { connect } from 'react-redux';

import Chart from '../components/chart';

class ResultList extends Component{

    render(){
        return(
            <div>
                <table className="table ">
                    <thead>
                    <tr>
                        <th>City</th>
                        <th>Temperature (K) </th>
                        <th>Pressure (hPa) </th>
                        <th>Humidity (%) </th>
                        <th>Clouds (%) </th>
                        <th>Wind Speed (meter/sec) </th>
                    </tr>
                    </thead>

                    <tbody>
                    {this.props.weather.map(this.renderTable)}
                    </tbody>

                </table>
            </div>
        );//return
    }//render

    renderTable(data){

        const cityName = data.city.name;
        const temp = data.list.map(listData => listData.main.temp);
        const pressure = data.list.map(listData => listData.main.pressure);
        const humidity = data.list.map(listData => listData.main.humidity);
        const clouds = data.list.map(listData => listData.clouds.all);
        const windSpeed = data.list.map(listData => listData.wind.speed);

        return(
            <tr key={data.city.id}>
                <td><b> {cityName} </b></td>
                <td><Chart data={temp} color="red" units="K" /></td>
                <td><Chart data={pressure} color="blue" units="hPa" /></td>
                <td><Chart data={humidity} color="green" units="%" /></td>
                <td><Chart data={clouds} color="orange" units="%" /></td>
                <td><Chart data={windSpeed} color="grey" units="m/s" /></td>
            </tr>
        );
    }
}//class

function mapStateToProps(state) {
    return {
        weather: state.weather
    }
}
export default connect (mapStateToProps)(ResultList);