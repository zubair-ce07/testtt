import React from "react";
import "./Employee.css";
import djangoapi from "../djangoapi";

class Employee extends React.Component {
  constructor() {
    super();
    this.listDirects = this.listDirects.bind(this);
    this.state = {
      directs: []
    };
  }

  listDirects(username) {
    djangoapi.getDirects(username, jsonData => {
      this.setState({
        directs: jsonData.directs
      });
    });
  }

  render() {
    return (
      <div>
        <p>
          {this.props.emp.first_name}
        </p>
        <a href="#" onClick={() => this.listDirects(this.props.emp.username)}>
          {this.props.emp.directs}
        </a>
        {this.state.directs !== []
          ? this.state.directs.map(current => {
              return <Employee emp={current} />;
            })
          : null}
      </div>
    );
  }
}

export default Employee;
