import React, { Component } from "react";
import Modal from "./Modal.js";
import "./Task.css";

class Task extends Component {
  constructor(props) {
    super();
    this.toggleModal = this.toggleModal.bind(this);
    this.state = {
      id: props.id,
      description: props.value,
      modalOpen: false
    };
  }

  toggleModal() {
    this.setState({
      modalOpen: !this.state.modalOpen
    });
  }

  toggleCompletion() {
    var temp = JSON.parse(localStorage.getItem(this.state.id));
    temp.status = temp.status === "complete" ? "pending" : "complete";
    localStorage.setItem(this.state.id, JSON.stringify(temp));
    this.toggleModal();
    this.props.storage();
  }

  render() {
    return (
      <li className="task">
        <a href="#" onClick={this.toggleModal.bind(this)}>
          {this.state.description}
        </a>
        <Modal
          show={this.state.modalOpen}
          toggleTask={this.toggleCompletion.bind(this)}
          onClose={this.toggleModal}
        />
      </li>
    );
  }
}

export default Task;
