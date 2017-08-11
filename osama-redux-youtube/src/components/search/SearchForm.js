import React, { Component } from "react";
import "./SearchForm.css";

class SearchForm extends Component {
  handleSubmit = evt => {
    evt.preventDefault();
    const inputValue = evt.target.elements.query.value;
    if (!inputValue.trim()) {
      return;
    }
    this.props.startSearchRequest(inputValue);
  };

  render() {
    return (
      <div className="search-container">
        <form
          id="search-form"
          className="search-form"
          onSubmit={evt => this.handleSubmit(evt)}
        >
          <input
            name="query"
            className="search-input"
            type="text"
            placeholder="Search"
          />
          <button type="submit" className="search-button">
            Search
          </button>
        </form>
      </div>
    );
  }
}

export default SearchForm;
