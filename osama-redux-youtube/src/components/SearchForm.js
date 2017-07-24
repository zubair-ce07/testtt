import React, { Component } from "react";
import { Route, Link } from "react-router-dom";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import "./SearchForm.css";

import { searchYoutube } from "../actions";

let SearchForm = ({ dispatch }) => {
  let input = "";

  return (
    <div className="search-container">
      <form
        id="search-form"
        className="search-form"
        onSubmit={evt => {
          evt.preventDefault();
          if (!input.value.trim()) {
            return;
          }
          dispatch(searchYoutube(input.value));
          input.value = "";
        }}
      >
        <input
          ref={node => {
            input = node;
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
};

SearchForm = connect()(SearchForm);

export default SearchForm;
