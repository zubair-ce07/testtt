import React, { Component } from "react";

import Table from "react-bootstrap/Table";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { TableHeader } from '../table-header';
import { CourseRow } from './Course-row';
import { CourseHeaderRow } from './Course-header-row';

import API from "../../api";


const courseHeaders = [
 { id: 1, name: "Course Code"}, 
 { id: 2, name: "Course Name"}, 
 { id: 3, name: "Cred Hrs"}
];

export class Course extends Component {
  state = { semesters: [] };
  componentDidMount() {
    const id = this.props.match.params.id;
    API.get(`programs/${id}/semesters/`).then(({ data }) => {
      const semesters = data;
      this.setState({ semesters });
    });
  }
  renderCourses = () => (
    <Container>
      <Row>
        {this.state.semesters.map(semester => (
          <React.Fragment key={semester.id}>
            <Col md={6}>
              <Table striped bordered hover variant="dark">
                <thead>
                  <tr>
                    {courseHeaders.map(header => (
                      <TableHeader key={header.id} header={header} />
                    ))}
                  </tr>
                </thead>
                <tbody>
                 <CourseHeaderRow semester={semester} />
                  {semester.semester_courses.map(course => (
                    <CourseRow key={course.id} course={course} ></CourseRow>
                  ))}
                </tbody>
              </Table>
            </Col>
          </React.Fragment>
        ))}
      </Row>
    </Container>
  );

  render() {
    return this.renderCourses();
  }
}
