import React from 'react';
import fusioncharts from 'fusioncharts';
import charts from 'fusioncharts/fusioncharts.charts';
import ReactFC from 'react-fusioncharts';
charts(fusioncharts);

class  WeatherChart extends React.Component {
    calculateAverage(weatherData, key){
        return Math.ceil(weatherData.list.map(data => data.main[key]).reduce((a,b) => a + b) / weatherData.list.length)
    }

    render(){
        const dataSource = {
            chart: {
                caption: "Weather Chart For " + this.props.data.city.name,
                theme: "ocean"
            },
            data: [ {
                label: "Temperature",
                value: this.calculateAverage(this.props.data, 'temp')
            }, {
                label: "Pressure",
                value: this.calculateAverage(this.props.data, 'pressure')
            }, {
                label: "Humidity",
                value: this.calculateAverage(this.props.data, 'humidity')
            }]
        };

        const chartConfigs = {
            renderAt: "revenue-chart-container",
            type: "column2d",
            width: 400,
            height: 600,
            dataFormat: "json",
            dataSource: dataSource
        };
        return (
            <div>
                <ReactFC {...chartConfigs} />
                <br/>
            </div>
        );
    }
}
export default WeatherChart;
