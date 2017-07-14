import React, { Component } from "react";
import Task from './Task.js'
import "./App.css";

class App extends Component {
  constructor() {
    super();
    this.getCount = this.getCount.bind(this);
    this.getTask = this.getTask.bind(this);
    this.getTaskList = this.getTaskList.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.addTask = this.addTask.bind(this);
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
    console.log(taskList);
    this.setState({
      count: this.state.count + 1,
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
    const taskList = this.state.tasks.map((task, id) => {
      if (task.status === this.state.filter || this.state.filter === "all") {
        return (
          <Task
            key={id}
            id={task.id}
            value={task.description}
            storage={this.storageChange.bind(this)}
          />
        );
      }
    });
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
          <input
            type="radio"
            onClick={this.handleRadioChange.bind(this)}
            name="status"
            value="pending"
            defaultChecked
          />
          <span>Pending</span>
          <input
            type="radio"
            onClick={this.handleRadioChange.bind(this)}
            name="status"
            value="complete"
          />
          <span>Completed</span>
          <input
            type="radio"
            onClick={this.handleRadioChange.bind(this)}
            name="status"
            value="all"
          />
          <span>All</span>
        </form>
        <ul>
          {taskList}
        </ul>
      </div>
    );
  }
}

export default App;
