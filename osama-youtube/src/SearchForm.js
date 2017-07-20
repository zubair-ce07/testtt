import React, { Component } from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import "./SearchForm.css";

class SearchForm extends Component {
  constructor() {
    super();
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.state = {
      query: ""
    };
  }

  static propTypes = {
    searchHandler: PropTypes.func
  };

  handleChange(query) {
    this.setState({
      query
    });
  }

  handleSubmit(evt) {
    evt.preventDefault();
    this.props.searchHandler(this.state.query);
  }

  render() {
    return (
      <div className="search-container">
        <form action="" className="search-form">
          <input
            onChange={evt => this.handleChange(evt.target.value)}
            className="search-input"
            type="text"
            placeholder="Search"
          />
          <Link to="/search">
            <button
              onClick={this.handleSubmit}
              className="search-button"
              type="submit"
            >
              Search
            </button>
          </Link>
        </form>
      </div>
    );
  }
}

export default SearchForm;
