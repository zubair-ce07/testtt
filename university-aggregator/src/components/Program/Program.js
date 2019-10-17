import React, { Component } from "react";

import Table from "react-bootstrap/Table";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { TableHeader } from "../table-header";
import { ProgramRow } from "./program-row";

import API from "../../api";


const programHeaders = [
  { id: 1, name: "Programs" },
  { id: 2, name: "Branches" }
];

export class Program extends Component {
  state = { programs: [] };

  constructor(props){
    super(props);
    this.navigateToCourses.bind(this)
  }

  componentDidMount() {
    const id = this.props.match.params.id;
    API.get(`institutions/${id}/programs/`).then(({ data }) => {
      const programs = data;
      this.setState({ programs });
    });
  }
  navigateToCourses = id => {
    this.props.history.push(`/programs/${id}/courses/`);
  };
  renderPrograms = () => (
    <Container>
      <Row>
        <Col md={12}>
          <Table striped bordered hover variant="dark">
            <thead>
              <tr>
                {programHeaders.map(header => (
                  <TableHeader key={header.id} header={header} />
                ))}
              </tr>
            </thead>
            <tbody>
              {this.state.programs.map(program => (
                <ProgramRow
                  key={program.id}
                  program={program}
                  navigate={this.navigateToCourses}
                />
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

