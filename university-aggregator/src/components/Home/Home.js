import React, { Component } from "react";

import Form from "react-bootstrap/Form";

import {api} from "../.././utils/api";

export class Home extends Component {
  state = {
    institutions: []
  };
  componentDidMount() {
    api.get(`institutions/`).then(({data : institutions}) => {
      this.setState({ institutions });
    })
    .catch((error) => {
      console.log('error', error);
      // todo show toast
    })
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


