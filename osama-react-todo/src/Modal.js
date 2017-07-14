import React, { Component } from "react";
import "./Modal.css";

class Modal extends Component {
  constructor(props) {
    super();
  }
  render() {
    return (
      <div className="backdrop">
        <div className="modal">
          <h2>Do you want to toggle this task?</h2>
          <h3>
            Task: {this.props.description}
          </h3>
          <button onClick={this.props.toggleTask}>Yes</button>
          <button onClick={this.props.onClose}>No</button>
        </div>
      </div>
    );
  }
}

export default Modal;
