import React, {Component} from 'react'
import WeatherChart from '../components/weatherChart';
import {connect} from 'react-redux';

class WeatherChartList extends Component {
    render(){
        const WeatherCharts = this.props.weather_data.map( data => {
            return (<WeatherChart key={data.data.city.id} data={data.data} />);
        });
        return (
            <div>
                {WeatherCharts}
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


