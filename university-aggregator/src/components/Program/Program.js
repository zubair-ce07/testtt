import React, { Component } from "react";

import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { AppTable } from "../common/table";

import { api } from "../.././utils/api";
import { programHeaders } from "../../utils/contants";

export class Program extends Component {
  state = { programs: [] };

  constructor(props) {
    super(props);
    this.navigateToCourses.bind(this);
  }

  componentDidMount() {
    const id = this.props.match.params.id;
    api
      .get(`institutions/${id}/programs/`)
      .then(({ data: programs }) => {
        this.setState({ programs });
      })
      .catch(error => {
        console.log("error", error);
        // todo show toast
      });
  }
  navigateToCourses = id => {
    console.log("id");
    this.props.history.push(`/programs/${id}/courses/`);
  };

  render() {
    return (
      <Container>
        <Row>
          <Col md={12}>
            <AppTable
              headers={programHeaders}
              navigate={this.navigateToCourses}
              data={this.state.programs}
              type={"programs"}
            />
          </Col>
        </Row>
      </Container>
    );
  }
}
