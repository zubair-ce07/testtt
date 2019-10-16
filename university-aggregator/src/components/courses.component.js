import React, { Component } from "react";

import Table from "react-bootstrap/Table";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import API from "../api";

const courseHeaders = ["Course Code", "Course Name", "Cred Hrs"];

export class Course extends Component {
  state = { semesters: [] };
  componentDidMount() {
    const id = this.props.match.params.id;
    API.get(`programs/${id}/semesters/`).then(({data}) => {
      const semesters = data;
      this.setState({ semesters });
    });
  }
  renderCourses = () => (
    <Container>
      <Row>
        <Col md={6}>
          <Table striped bordered hover variant="dark">
            <thead>
              <tr>
                {courseHeaders.map(header => (
                  <th>{header}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {this.state.semesters.map(semester => (
                <React.Fragment key={semester.id}>
                  <tr>
                    <td colSpan={6}>
                      <h5>
                        <strong>Semester {semester.number}</strong>
                      </h5>
                    </td>
                  </tr>
                  {semester.semester_courses.map(course => (
                    <tr>
                      <td>
                        <span>{course.code}</span>
                      </td>
                      <td>
                        <span>{course.name}</span>
                      </td>
                      <td>
                        <span>{course.credit_hour}</span>
                      </td>
                    </tr>
                  ))}
                </React.Fragment>
              ))}
            </tbody>
          </Table>
        </Col>
      </Row>
    </Container>
  );

  render() {
    return this.renderCourses();
  }
}
