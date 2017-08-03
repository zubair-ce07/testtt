import React from "react";
import "./Employee.css";

class Employee extends React.Component {
  constructor() {
    super();
  }

  render() {
    return (
      <div className="circle">
        <p>{this.props.emp.first_name.charAt(0) + this.props.emp.last_name.charAt(0)}</p>
      </div>
    );
  }
}

export default Employee;
