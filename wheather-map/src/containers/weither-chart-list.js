import React, {Component} from 'react'
import WeatherChart from '../components/weather-chart';
import {connect} from 'react-redux';

class WeatherChartList extends Component {
    render(){
        const weatherCharts = this.props.weather_data.map( data => {
            return (<WeatherChart key={data.data.city.id} data={data.data} />);
        });
        return (
            <div>
                {weatherCharts}
            </div>
        );
    }
};

function mapStateToProps(state){
   return {
      weather_data: state.weatherData
    };
};
export default connect(mapStateToProps)(WeatherChartList);


