import React, { Component } from "react";
import Task from "./Task.js";
import "./App.css";

class App extends Component {
  constructor() {
    super();
    this.getCount = this.getCount.bind(this);
    this.getTask = this.getTask.bind(this);
    this.getTaskList = this.getTaskList.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleRadioChange = this.handleRadioChange.bind(this);
    this.addTask = this.addTask.bind(this);
    this.storageChange = this.storageChange.bind(this);
    this.state = {
      count: this.getCount(),
      tasks: this.getTaskList(),
      inputValue: "",
      filter: "pending"
    };
  }

  // gets a task object from localStorage
  getTask(index) {
    return JSON.parse(localStorage.getItem(+index));
  }

  getCount() {
    if (localStorage.getItem("count")) {
      return localStorage.getItem("count");
    } else {
      return 0;
    }
  }

  setCount(count) {
    localStorage.setItem("count", count);
  }

  getTaskList() {
    let tasks = [],
      count = this.getCount();
    for (let i = 0; i < count; i++) {
      var temp = this.getTask(i);
      tasks[i] = temp;
    }
    return tasks;
  }

  handleInputChange(evt) {
    this.setState({
      inputValue: evt.target.value
    });
  }

  handleRadioChange(evt) {
    this.setState({
      filter: evt.target.value
    });
  }

  addTask() {
    let task = {
      id: this.state.count,
      description: this.state.inputValue,
      status: "pending"
    };
    let taskList = this.getTaskList();
    localStorage.setItem(this.state.count, JSON.stringify(task));
    localStorage.setItem("count", ++this.state.count);
    taskList.push(task);
    this.setState({
      tasks: taskList
    });
    document.getElementById("todoInput").value = "";
  }

  storageChange() {
    this.setState({
      tasks: this.getTaskList()
    });
  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <h2>The 10001st Todo App</h2>
        </div>
        <p className="inputField">
          <input id="todoInput" type="text" onChange={this.handleInputChange} />
          <button onClick={this.addTask}>Add Task</button>
        </p>
        <form id="filterForm">
          {["pending", "complete", "all"].map((status, index) => {
            return (
              <span key={status}>
                <input
                  type="radio"
                  onClick={this.handleRadioChange}
                  name="status"
                  value={status}
                />
                <span className="capitalize">
                  {status}
                </span>
              </span>
            );
          })}
        </form>
        <ul>
          {this.state.tasks
            .filter(task => {
              return (
                task.status === this.state.filter || this.state.filter === "all"
              );
            })
            .map(task => {
              return (
                <Task
                  key={task.id}
                  id={task.id}
                  value={task.description}
                  storage={this.storageChange}
                />
              );
            })}
        </ul>
      </div>
    );
  }
}

export default App;
