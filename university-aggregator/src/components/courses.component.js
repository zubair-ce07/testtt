import React, { Component } from 'react'
import  API  from '../api';

export class Course extends Component {
    state={ courses : []}
    componentDidMount() {
      const id = this.props.match.params.id
      API.get(`programs/${id}/courses/`).then(res => {
        const courses = res.data;
        this.setState({ courses });
      });
    }
    renderCourses = ()  => (
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
                {this.state.courses.map(course => (
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
                    <td>
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

    render() {
    return this.renderCourses()
    }
}