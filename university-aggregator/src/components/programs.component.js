import React, { Component } from "react";

import Table from "react-bootstrap/Table";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import API from "../api";

const programHeaders = ["Programs", "Branches"];

export class Program extends Component {
  state = { programs: [] };

  componentDidMount() {
    const id = this.props.match.params.id;
    API.get(`institutions/${id}/programs/`).then(({data}) => {
      const programs = data;
      this.setState({ programs });
    });
  }
  navigateToCourses(id) {
    this.props.history.push(`/programs/${id}/courses/`);
  }
  renderPrograms = () => (
    <Container>
      <Row>
        <Col md={12}>
          <Table striped bordered hover variant="dark">
            <thead>
              <tr>
                {programHeaders.map(header => (
                  <th scope="col">{header}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {this.state.programs.map(program => (
                <React.Fragment key={program.id}>
                  <tr>
                    <td colSpan={6}>
                      <h4>
                        <strong>{program.category}</strong>
                      </h4>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <span onClick={id => this.navigateToCourses(program.id)}>
                        {program.name}
                      </span>
                    </td>
                    <td>
                      <span>{program.campus.name}</span>
                    </td>
                  </tr>
                </React.Fragment>
              ))}
            </tbody>
          </Table>
        </Col>
      </Row>
    </Container>
  );

  render() {
    return this.renderPrograms();
  }
}

