import React, { Component } from "react";
import "./SearchForm.css";

class SearchForm extends Component {
  render() {
    return (
      <div className="search-container">
        <form
          id="search-form"
          className="search-form"
          onSubmit={evt => {
            evt.preventDefault();
            if (!this.input.value.trim()) {
              return;
            }
            this.props.startSearchRequest(this.input.value);
            this.input.value = "";
          }}
        >
          <input
            ref={node => {
              this.input = node;
            }}
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
