import React from "react";
import "./Result.css";

class Result extends React.Component {
  constructor() {
    super();
    this.handleClick = this.handleClick.bind(this);
  }
  handleClick() {
      this.props.play(this.props.vidId);
  }
  render() {
    return (
      <div className="result" onClick={this.handleClick}>
        <img
          className="thumbnail"
          src={this.props.imgurl}
          alt={this.props.title}
        />
        <div className="detail">
          <h3 className="title">
            {this.props.title}
          </h3>
          <p className="description">
            {this.props.description}
          </p>
        </div>
      </div>
    );
  }
}

export default Result;
