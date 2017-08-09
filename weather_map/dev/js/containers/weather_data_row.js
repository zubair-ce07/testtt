import React from 'react';
import { connect } from "react-redux";
import Chart from '../components/chart';


class WeatherDataRow extends React.Component
{
    renderWeather(cityData)
    {
        const name = cityData.city.name;
        const id = cityData.city.id;
        const temps = cityData.list.map(data => { return data.main.temp });
        const pressures = cityData.list.map(data => { return data.main.pressure });
        const humidities = cityData.list.map(data => { return data.main.humidity });

        return (
            <tr key={id}>
                <td width={10 + '%'}><h3><strong>{name}</strong></h3></td>
                <td width={30 + '%'}> <Chart color="red" data={temps} unit={ String.fromCharCode(176) + 'C' } /> </td>
                <td width={30 + '%'}> <Chart color="green" data={pressures} unit="hPa"/> </td>
                <td width={30 + '%'}> <Chart color="black" data={humidities} unit="%" /> </td>
            </tr>
        )
    }

    render()
    {
        return (
            <tbody>
            {
                this.props.weather.map(this.renderWeather)
            }
            </tbody>
        )
    }
}

function mapStateToProps(state)
{
    return ({
        weather: state.weather.weather_data,
    })
}

export default connect(mapStateToProps)(WeatherDataRow);