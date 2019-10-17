import React, { Component } from "react";

import Form from "react-bootstrap/Form";

import API from '../../api'

export class Home extends Component {
  state = {
    institutions: []
  };
  componentDidMount() {
    API.get(`institutions/`).then(({data}) => {
      const institutions = data;
      this.setState({ institutions });
    });
  }
  getPrograms = event => {
    const id = event.target.value;
    this.props.history.push(`institutions/${id}/programs/`);
  };
  render() {
    return (
      <div>
        <h1>Choose University</h1>
        <Form.Group>
          <Form.Label>Choose University</Form.Label>
          <Form.Control as="select"  onChange={(event) => this.getPrograms(event)}>
            {this.state.institutions.map(institute => (
              <option value={institute.id} key={institute.id}>
                {institute.name}
              </option>
            ))}
          </Form.Control>
        </Form.Group>
      </div>
    );
  }
}


