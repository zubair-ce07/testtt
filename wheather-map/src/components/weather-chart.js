import React, {Component} from 'react';
import fusioncharts from 'fusioncharts';
import charts from 'fusioncharts/fusioncharts.charts';
import ReactFC from 'react-fusioncharts';
charts(fusioncharts)

class  WeitherChart extends Component {
    getTemperature(cityData){
        const temperatures = cityData.list.map(data=>{ return data.main.temp;});
        let sum = 0;
        for (let temperature of temperatures) {
            sum += temperature;
        }
        return Math.ceil(sum/temperatures.length);
    };

    getPressure(cityData){
       const pressures = cityData.list.map(data=>{ return data.main.pressure;});
        let sum = 0;
        for (let pressure of pressures) {
            sum += pressure;
        }
       return Math.ceil(sum/pressures.length)
    };

    getHumadity(cityData){
       const humadities = cityData.list.map(data=>{ return data.main.humidity;});
       let sum = 0;
        for (let humadity of humadities) {
            sum += humadity;
        }
        return Math.ceil(sum/humadities.length)+ '%';
    };

    render(){
        var myDataSource = {
        chart: {
            caption: "Weither Chart Of " + this.props.data.city.name,
            theme: "ocean"
        },
        data: [ {
            label: "Temperature",
            value: this.getTemperature(this.props.data)
        }, {
            label: "Pressure",
            value: this.getPressure(this.props.data)
        }, {
            label: "Humadity",
            value: this.getHumadity(this.props.data)
        }]
    };

    var revenueChartConfigs = {
        renderAt: "revenue-chart-container",
        type: "column2d",
        width: 300,
        height: 200,
        dataFormat: "json",
        dataSource: myDataSource
    };
        return (
            <div>
                 <ReactFC {...revenueChartConfigs
                         } /> <br/>
            </div>
        );
    }
}
export default WeitherChart;