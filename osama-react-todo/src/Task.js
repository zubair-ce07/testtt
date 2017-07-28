import React, { Component } from "react";
import Modal from "./Modal.js";
import "./Task.css";

class Task extends Component {
  constructor(props) {
    super();
    this.toggleModal = this.toggleModal.bind(this);
    this.toggleCompletion = this.toggleCompletion.bind(this);
    this.state = {
      id: props.id,
      description: props.value,
      modalOpen: false
    };
  }

  toggleModal() {
    this.setState((prevState, props) => ({
      modalOpen: !prevState.modalOpen
    }));
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
        <a onClick={this.toggleModal}>
          {this.state.description}
        </a>
        {this.state.modalOpen &&
          <Modal
            show={this.state.modalOpen}
            toggleTask={this.toggleCompletion}
            onClose={this.toggleModal}
            description={this.state.description}
          />}
      </li>
    );
  }
}

export default Task;
