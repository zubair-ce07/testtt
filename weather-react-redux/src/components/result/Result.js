import React, { Component } from 'react';
import Chart from '../Chart/chart';


class Result extends Component {

    render() {
        var weather = this.props.weather;

        return (
            <div>
                {
                    <div>
                        {weather.slice(0).reverse().map((city) => {
                            return (
                                <div>
                                    <h1>Weather for: {city.city.name}</h1>
                                    <Chart
                                        data={city}
                                    />
                                </div>
                            );
                        })}
                    </div>
                }
            </div>
        )
    }
}

export default Result;