import React from "react";
import "./Appraisal.css";

class Appraisal extends React.Component {
  render() {
    return (
      <div className="appraisal">
        <p className="appraisal-title">
          {this.props.data.year + " Rating: " + this.props.data.rating + "/5"}
        </p>
        <p className="appraisal-description">
          {this.props.data.description}
        </p>
      </div>
    );
  }
}

export default Appraisal;
