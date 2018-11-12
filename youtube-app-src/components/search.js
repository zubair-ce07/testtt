import React, { Component } from 'react';


class Search extends Component {
  handleSearchButtonClick(){
    let query = document.getElementById("searchInput").value
    this.props.onClick(query)
  }

  render() {
    return (
      <nav className="navbar navbar-light bg-light search-panel">
        <label className="navbar-brand">
          Pacifico Player
        </label>
        <div className="form-inline">
          <input
            className="form-control mr-sm-2"
            type="text"
            placeholder="Search"
            aria-label="Search"
            id="searchInput"
          />
          <button
            className="btn btn-outline-success my-2 my-sm-0"
            onClick={this.handleSearchButtonClick.bind(this)}
          >
            Search
          </button>
        </div>

      </nav>
    )
  }
}


export default Search;
