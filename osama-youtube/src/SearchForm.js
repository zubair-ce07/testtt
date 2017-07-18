import React, { Component } from "react";
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

  handleChange(evt) {
    this.setState({
      query: evt.target.value
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
            onChange={this.handleChange}
            className="search-input"
            type="text"
            placeholder="Search"
          />
          <button
            onClick={this.handleSubmit}
            className="search-button"
            type="submit"
          >
            Search
          </button>
        </form>
      </div>
    );
  }
}

export default SearchForm;
