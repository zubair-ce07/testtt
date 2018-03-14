import React, { Component } from 'react';
import { Link } from 'react-router-dom'
import {loadWeatherData} from "../actions/weather";
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import autoBind from 'react-autobind';

class Search extends Component {

    constructor(props) {
        super(props);
        autoBind(this);
        this.state = {query:''};
        console.log(props)
        // This binding is necessary to make `this` work in the callback
        this.handleChange = this.handleChange.bind(this);
        this.handleOnClick = this.handleOnClick.bind(this);
    }
    handleChange(event) {
        this.setState({query: event.target.value});
    }
    handleOnClick() {
        console.log(this.props)
       this.props.dispatch(loadWeatherData(this.state.query));
        console.log(this.props)
    }

    render() {
        return (
            <div style={{paddingLeft:50,paddingTop:10}}>
                <input id='query' name='query' value={this.state.query}  onChange={this.handleChange} type='text'/>
                    <button id='search-button' name='search-button' onClick={(event) => this.handleOnClick(event)}> Search</button>
            </div>

        );
    }
}

export default connect()(Search);