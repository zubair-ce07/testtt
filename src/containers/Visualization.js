import React, { Component } from 'react';
import { connect } from 'react-redux';
const ReactHighcharts = require('react-highcharts');

class Visualization extends Component {

    render(){
        return (
            <div className='container'>
              <ReactHighcharts config={this.props.weather}/>
            </div>
        )
    }
}
function mapStateToProps(state){
    return {
        weather: state.weather
    };
}
export default connect(mapStateToProps)(Visualization);