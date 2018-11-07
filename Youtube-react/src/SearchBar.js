import React, { Component } from 'react';
import { Button, InputGroup, InputGroupAddon } from 'reactstrap';
import Autosuggest from 'react-autosuggest';
import axios from 'axios';
import './App.css';

const searchWidth = {
  'width': 1200,
  'margin-left': 30,
};

const apiUrl = 'https://www.googleapis.com/youtube/v3/'
const key = 'AIzaSyCv3KW6DhugN2yfS5HfN97tOt4525SDyio'
const maxResults = 5
const type = 'video'
const part = 'snippet'


class SearchBar extends Component {
  state = {
    'value': this.props.query,
    'suggestions': [],
  }

  onSuggestionsFetchRequested = ({ value }) => {
    let query = value;
    let url = `${apiUrl}search?maxResults=${maxResults}&part=${part}&order=viewCount&q=${query}&type=${type}&videoDefinition=high&key=${key}`

    axios.get(url)
      .then(response => {
        this.setState({ 'suggestions': response.data.items, });
      });
  }

  onSuggestionsClearRequested = () => {
    this.setState({ 'suggestions': [], });
  }

  getSuggestionValue = data => {
    return data.snippet.title;
  }

  renderSuggestion(suggestion, { query }) {
    return (
      <div>
        <span className='suggestion-content'>
          <span >
            <span>{suggestion.snippet.title}</span>
          </span>
        </span>
      </div>
    );
  }

  onChange = (event, { newValue, method }) => {
    this.setState({
      value: newValue
    });
    this.props.onChange(newValue);
  };

  render() {
    const size = {
      'width': 1100,
      'height': 50,
    }

    let { value } = this.state;
    const inputProps = {
      placeholder: 'Youtube Search',
      value,
      onChange: this.onChange,
      style: size,
    };


    return (

      <InputGroup style={searchWidth}>
        <Autosuggest
          suggestions={this.state.suggestions}
          onSuggestionsFetchRequested={this.onSuggestionsFetchRequested}
          onSuggestionSelected={this.props.searchClick}
          onSuggestionsClearRequested={this.onSuggestionsClearRequested}
          getSuggestionValue={this.getSuggestionValue}
          renderSuggestion={this.renderSuggestion}
          inputProps={inputProps}
        />

        <InputGroupAddon addonType="append">
          <Button color="secondary" onClick={this.props.searchClick}>Search</Button>
        </InputGroupAddon>
      </InputGroup>
    );
  }
}

export { SearchBar };