import React, { Component } from 'react';
import './App.css';
import { Link } from 'react-router-dom'


class Search extends Component {

    constructor(props) {
        super(props);
        this.state = {query:''};
        // This binding is necessary to make `this` work in the callback
        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(event) {
        this.setState({query: event.target.value});
    }

    render() {
        return (
            <div style={{paddingLeft:50,paddingTop:10}}>
                <input id='query' name='query' value={this.state.query}  onChange={this.handleChange} type='text'/>
                <Link to={`/search/${this.state.query}`}>
                    <button id='search-button' name='search-button'>Search</button>
                </Link>
            </div>

        );
    }
}


export default Search
