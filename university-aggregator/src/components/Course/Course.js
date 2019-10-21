import React, { Component } from "react";

import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { AppTable } from '../common/table';

import {api} from "../.././utils/api";
import { courseHeaders } from "../../utils/contants";


export class Course extends Component { 
  state = { semesters: [] };
  componentDidMount() {
    const id = this.props.match.params.id;
    api.get(`programs/${id}/semesters/`).then(({ data : semesters }) => {
      this.setState({ semesters });
    })
    .catch((error) => {
      console.log('error', error);
      // todo show toast
    })
  }

  render() {
    return (
      <Container>
        <Row>
          {this.state.semesters.map(semester => (
            <div key={semester.id}>
              <Col md={6}>
                <AppTable headers={courseHeaders} data={semester} type={'course'} />
              </Col>
            </div>
          ))}
        </Row>
      </Container>
    )
  }
}

