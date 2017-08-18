import React from 'react';
import { Table } from 'react-bootstrap';

import WeatherDataRow from '../containers/weather_data_row';
import '../../scss/style.scss';


class WeatherDataList extends React.Component
{
    render()
    {
        return (
            <Table responsive bordered condensed hover>
                <thead>
                <tr>
                    <th>City</th>
                    <th>Temperature</th>
                    <th>Pressure</th>
                    <th>Humidity</th>
                </tr>
                </thead>
                <WeatherDataRow/>
            </Table>
        )
    }
}

export default WeatherDataList;