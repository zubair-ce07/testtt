import React, { Component } from "react";
import "./Modal.css";

class Modal extends Component {
  constructor() {
    super();
  }
  render() {
    console.log(this.props.show);
    if (!this.props.show) {
      return null;
    }
    return (
      <div className="backdrop">
        <div className="modal">
          <h2>this is a modal</h2>
          <button onClick={this.props.toggleTask}>Yes</button>
          <button onClick={this.props.onClose}>No</button>
        </div>
      </div>
    );
  }
}

export default Modal;
