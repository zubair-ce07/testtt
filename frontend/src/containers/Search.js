import React, { Component } from 'react';
import {loadCategory} from '../actions/category';
import { connect } from 'react-redux';

class Search extends Component {

    constructor(props) {
        super(props);
        this.state = {query:''};

        this.handleChange = this.handleChange.bind(this);
        this.handleOnClick = this.handleOnClick.bind(this);
    }
    handleChange(event) {
        this.setState({query: event.target.value});
    }
    handleOnClick() {
       this.props.dispatch(loadCategory(this.state.query));
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