import React, { Component } from 'react';
import AppEnhancer from './App.enhancer';


class App extends Component {
  componentDidMount() {
    this.props.simpleAction()
  }
  render() {
    const { result } = this.props;

    return (
      <div>
        <h1>Redux Setup</h1>
        <p>{result}</p>
      </div>
    );
  }
}

export default AppEnhancer(App);
