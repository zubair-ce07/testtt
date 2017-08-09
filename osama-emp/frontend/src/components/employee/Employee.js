import React from "react";
import "./Employee.css";
import djangoapi from "../../djangoapi";

class Employee extends React.Component {
  constructor(props) {
    super();
    this.state = {
      directs: []
    };
  }

  listEmployees(evt) {
    evt.preventDefault();
    if (this.state.directs.length === 0) {
      djangoapi.getDirects(this.props.emp.username, jsonData => {
        this.setState({
          directs: jsonData.directs
        });
      });
    } else {
      this.setState({
        directs: []
      });
    }
  }

  render() {
    return (
      <div>
        <li>
          Name:
          <a
            href=""
            onClick={evt => {
              evt.preventDefault();
              this.props.profileHandler(this.props.emp.username);
            }}
          >
            {this.props.emp.first_name + " " + this.props.emp.last_name}
          </a>
        </li>
        {this.props.emp.reports_to === localStorage.username
          ? <li>Give Appraisal:</li>
          : null}
        <li>
          <a href="" onClick={evt => this.listEmployees(evt)}>
            Directs
          </a>
        </li>
        <ul>
          {this.state.directs !== []
            ? this.state.directs.map(current => {
                return (
                  <Employee
                    key={current.username}
                    emp={current}
                    profileHandler={this.props.profileHandler}
                  />
                );
              })
            : null}
        </ul>
      </div>
    );
  }
}

export default Employee;
