import React, { Component } from 'react';

import SearchBar from '../containers/search_bar';
import List from '../containers/result_list';

export default class App extends Component {
  render() {
    return (
      <div>
        <SearchBar />
        <List />
      </div>
    );
  }
}
