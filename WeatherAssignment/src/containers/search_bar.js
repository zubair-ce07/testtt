import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import { getWeather } from '../actions/index';

class SearchBar extends Component{

    constructor(props){
        super(props);
        this.state = {
            cityName: ""
        };
        this.onTextChange = this.onTextChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }//constructor

    onTextChange(event){
        this.setState({cityName: event.target.value });
    }

    onSubmit(event){
        event.preventDefault();
        this.props.getWeather(this.state.cityName);
        this.setState({cityName: '' });
    }

    render(){
        return(
            <div>
                <form onSubmit={this.onSubmit} className="input-group">
                    <input
                        placeholder="Enter city name here"
                        className="form-control"
                        value={this.state.cityName}
                        onChange={this.onTextChange}
                    />
                    <span className="input-group-btn">
                        <button type="submit" className="btn btn-primary">Search</button>
                    </span>
                </form>
            </div>
        );
    }//render

}//class


function mapDispatchToProps(dispatch) {
    return bindActionCreators ({ getWeather },dispatch);
}//mapDispatchToProp

export default connect (null, mapDispatchToProps)(SearchBar);
