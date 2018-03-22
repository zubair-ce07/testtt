import React, { Component } from 'react';
import './App.css';
import { Link } from 'react-router-dom'
import PropTypes from 'prop-types';


class Search extends Component {

    constructor(props) {
        super(props);

        this.handleChange = this.handleChange.bind(this);
        this.handleClick = this.handleClick.bind(this);
    }
    handleChange(e) {

        this.props.onSearchChange(e.target.value)
    }
    handleClick() {

        this.props.onSearchClick()
    }

    render() {

        const query=this.props.query;
        return (
            <div style={{paddingLeft:50,paddingTop:10}}>
                <input  value={query}  onChange={this.handleChange} />
                <Link to={`/search/${query}`} >
                    <button id='search-button' name='search-button' onClick={this.handleClick}>Search</button>
                </Link>
            </div>

        );
    }
}
Search.propTypes = {
    query:PropTypes.string,
    onSearchChange:PropTypes.func,
    onSearchClick:PropTypes.func
};

export default Search
