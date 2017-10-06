import React, { Component } from 'react';
import { Line } from 'react-chartjs-2';


class Chart extends Component {

    generateColor() {
        return 'rgb(' + Math.floor(Math.random() * 256) + ', ' + Math.floor(Math.random() * 256) + ', ' + Math.floor(Math.random() * 256) + ')';
    }

    render() {

        let labels = [];
        let temp = [];
        let pressure = [];
        let humid = [];

        this.props.data.list.forEach(record => {
            labels.push(record.dt_txt);
            temp.push(record.main.temp);
            pressure.push(record.main.pressure);
            humid.push(record.main.humidity);
        });

        return (
            <div>
                <Line data=
                    {{
                        labels, datasets: [{ borderColor: this.generateColor(), label: 'Temperature', data: temp }]
                    }}
                    width={100}
                    height={30}
                />

                <Line data=
                    {{
                        labels, datasets: [{ borderColor: this.generateColor(), label: 'Pressure', data: pressure }]
                    }}
                    width={100}
                    height={30}
                />

                <Line data=
                    {{
                        labels, datasets: [{ borderColor: this.generateColor(), label: 'Humidity', data: humid }]
                    }}
                    width={100}
                    height={30}
                />

            </div>
        );
    }
}


export default Chart;