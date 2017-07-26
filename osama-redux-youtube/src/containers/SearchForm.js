import React, { Component } from "react";

import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import "./SearchForm.css";

import { startSearchRequest } from "../actions";

class SearchForm extends Component {
  constructor(props) {
    super();
    this.input = "";
    this.dispatch = props.dispatch;
  }

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

function mapDispatchToProps(dispatch) {
  return bindActionCreators({ startSearchRequest: startSearchRequest }, dispatch);
}

export default connect(null, mapDispatchToProps)(SearchForm);
