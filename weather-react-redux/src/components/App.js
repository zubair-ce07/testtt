import React, { Component } from 'react';
import SearchBar from './SearchBar/SearchContainer';
import Result from './result/ResultContainer';
import './App.css';

class App extends Component {
  render() {
    return (
      <div>
        <SearchBar />
        <Result />
      </div>
    );
  }
}

export default App;
