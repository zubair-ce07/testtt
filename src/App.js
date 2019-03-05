import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header>
      </div>
    );

import React, {Component} from 'react';
import Table from './table';
import Form from './form';
class App extends Component {
  state = {
      characters: []
   };

    render() {
        return (
            <div className="container">
            <Table
              characterData={this.state.characters}
              removeCharacter={this.removeCharacter}
            />
            <Form
            handleSubmit={this.handleSubmit} />
            </div>
        );
    }

    handleSubmit = character => {
      this.setState({characters: [...this.state.characters, character]});
    }


    removeCharacter = index => {
    const { characters } = this.state;

    this.setState({
        characters: characters.filter((character, i) => {
            return i !== index;
        })
    });
  }
}

export default App;
