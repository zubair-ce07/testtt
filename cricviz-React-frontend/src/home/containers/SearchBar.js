import React, {Component} from 'react';
import {Button} from 'react-bootstrap';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import {fetchTeams} from '../actions/FetchTeams';

class SearchBar extends Component {
  constructor(props) {
    super(props);

    this.state = {term: ''};

    this.onInputChange = this.onInputChange.bind(this);
    this.onFormSubmit = this.onFormSubmit.bind(this);
  }

  onInputChange(event) {
    this.setState({term: event.target.value})
  }

  onFormSubmit(event) {
    event.preventDefault();
    //make the api call here
    this.props.fetchTeams(this.state.term);
    console.log(this.props.fetchTeams(this.state.term));
    this.setState({ term: '' });
  }

  render() {
    return (
      <form onSubmit={this.onFormSubmit} className="input-group">
        <input
          placeholder="Search players/teams"
          className="form-control"
          value={this.state.term}
          onChange={this.onInputChange} />
        <span className="input-group-button">
          <Button className="btn btn-info" bsStyle="primary" type="submit" >Search</Button>
        </span>
      </form>
    );
  }
}
// make sure that the action dispatched by the ActionCreator goes down to
// middleware then to reducers inside the app
function mapDispatchToProps(dispatch) {
  return bindActionCreators({ fetchTeams }, dispatch);
}

// pass null in place of the state as this container doesnt care about it here
export default connect(null, mapDispatchToProps)(SearchBar);
