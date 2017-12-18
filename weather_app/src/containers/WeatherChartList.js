import React, {Component} from 'react'
import WeatherChart from '../components/WeatherChart.js';
import {connect} from 'react-redux';

class WeatherChartList extends Component {
    render(){
        return (
            <div>
                {
                    this.props.weather_data.map( data => <WeatherChart key={data.city.id} data={data} />)
                }
            </div>
        );
    }
}

function mapStateToProps(state){
    return {
        weather_data: state
    };
}

export default connect(mapStateToProps)(WeatherChartList);
