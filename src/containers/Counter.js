import React, { Component } from 'react';
import { connect } from 'react-redux';

class Counter extends Component {
    constructor(props){
        super(props);
    }
    render(){
        return (
            <div className="cotainer">
                <div className="notification">
                    <h1>
                        {this.props.weather.title}
                    </h1>
                </div>
            </div>
        )
    }
}
function mapStateToProps(state){
    console.log(state)
    return {
        weather: state.weather,
    };
}
export default connect(mapStateToProps)(Counter);