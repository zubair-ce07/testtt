import React, { Component } from 'react';
import { connect } from 'react-redux';
import _ from 'underscore'

const ReactHighcharts = require('react-highcharts');

class Visualization extends Component {
    constructor(props){
        super(props);
        console.log(this.props)

    }

    render(){
        return (
            <div className="cotainer">
                <div className="notification">
                    <h1>

                    </h1>
                </div>

              <ReactHighcharts config={this.props.weather} ref="chart"></ReactHighcharts>
            </div>
        )
    }
}
function mapStateToProps(state){
    console.log(state)
    return {
        weather: state.weather
    };
}
export default connect(mapStateToProps)(Visualization);