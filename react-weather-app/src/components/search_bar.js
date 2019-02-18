import React, { Component } from 'react';
import { connect } from 'react-redux';

import * as actions from '../actions';

class SearchBar extends Component {
    constructor(props) {
        super(props)
        this.state = { term: '' };
    }

    onInputChange(event) {
        this.setState({ term: event.target.value });
    }

    onFormSubmit(event) {
        event.preventDefault();

        if (this.state.term) {
            this.props.fetchWeather(this.state.term);
            this.setState({ term: '' });
        }
    }

    render() {
        return (
            <form className='input-group' onSubmit={this.onFormSubmit.bind(this)}>
                <input 
                    placeholder="Search weather details by city name" 
                    className="form-control"
                    value={this.state.term} 
                    onChange={this.onInputChange.bind(this)} />
                <span className="input-group-btn">
                    <button className="btn btn-secondary" type="submit">Search</button>
                </span>
            </form>
        );
    }
}

export default connect(null, actions)(SearchBar);
