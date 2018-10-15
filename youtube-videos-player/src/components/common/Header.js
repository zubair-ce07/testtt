import React, { Component } from 'react';
import { func } from 'prop-types';

class Header extends Component {
  // Header component

  submit = (event) => {
    event.preventDefault();
    const query = event.target.search.value;
    if (query)
      this.props.searchOnYoutube(query);
  };

  render() {
    return (
      <div className="header">
        <div className="search-bar">
          <div className="youtube-logo">Youtube</div>
          <div className="header-input-wrapper col-md-6">
            <form className="fixed" onSubmit={this.submit}>
              <span className='input-span'>
                  <input placeholder="Type something" name="search"/>
                  <button className="submit-input">
                      <span className="glyphicon glyphicon-search"></span>
                  </button>
              </span>
            </form>
          </div>
        </div>
      </div>
    )
  }
}

Header.propTypes = {
  searchOnYoutube: func.isRequired,
};

export default Header
