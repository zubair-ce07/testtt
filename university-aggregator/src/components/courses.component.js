import React, { Component } from 'react'
import axios from "axios";
import { EndPoint } from '../config';

export class Course extends Component {
    state={ Courses : []}
    componentDidMount() {
      axios.get(EndPoint.courses).then(res => {
        const Courses = res.data;
        this.setState({ Courses });
      });
    }
    render() {
      return (
        <div className="container">
          <div className="row">
            <div className="col-md-6">
              <div className="table-responsive">
                <table className="table  table-bordered table-condensed table-hover table-striped">
                  <thead>
                    <tr>
                      <th>Course Code</th>
                      <th>Course Name</th>
                      <th>Cred Hrs</th>
                    </tr>
                  </thead>
                  <tbody>
                    {this.state.Courses.map(course => (
                     <React.Fragment key={course.id}> 
                      <tr>
                        <td colSpan={6}>
                          <h5>
                            <strong>Semester {course.semester}</strong>
                          </h5>
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <span>{course.code}</span>
                        </td>
                        <td>id
                          <span>{course.name}</span>
                        </td>
                        <td>
                          <span>{course.credit_hour}</span>
                        </td>
                      </tr>
                      </React.Fragment>  
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      );
    }
}