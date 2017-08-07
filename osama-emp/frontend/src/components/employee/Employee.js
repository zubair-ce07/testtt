import React from "react";
import "./Employee.css";
import djangoapi from "../../djangoapi";

class Employee extends React.Component {
  constructor() {
    super();
    this.state = {
      directs: []
    };
  }

  listDirects(username) {
    if (this.state.directs.length === 0) {
      djangoapi.getDirects(username, jsonData => {
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
        <p>
          {this.props.emp.first_name}
        </p>
        <a
          href="#"
          onClick={() => {
            this.listDirects(this.props.emp.username);
          }}
        >
          {this.props.emp.directs}
        </a>
        {this.state.directs !== []
          ? this.state.directs.map(current => {
              return <Employee key={current.username} emp={current} />;
            })
          : null}
      </div>
    );
  }
}

export default Employee;
