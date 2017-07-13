import React, { Component } from "react";
import logo from "./logo.svg";
import "./App.css";

class Task extends Component {
  constructor(props) {
    super();
    this.handleClick = this.handleClick.bind(this);
    this.state = {
      id: props.value.id,
      description: props.value.description,
      status: props.value.status
    };
  }

  handleClick(evt) {
    // window.confirm('Complete this task? \n"' + evt.target.innerHTML + '"')
    if (
      window.confirm('Complete this task? \n"' + evt.target.innerHTML + '"')
    ) {
      this.props.value.status = "complete";
    }
  }

  render() {
    return (
      <li className="task">
        <a href="#" onClick={this.handleClick}>
          {this.state.description}
        </a>
      </li>
    );
  }
}

class App extends Component {
  constructor() {
    super();
    this.getTaskList = this.getTaskList.bind(this);
    this.setTaskList = this.setTask.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.addTask = this.addTask.bind(this);
    this.state = {
      count: Boolean(localStorage.getItem("count"))
      ? localStorage.getItem("count")
      : 1,
      tasks: this.getTaskList(),
      inputValue: ""
    };
  }

  getTaskList() {
    var tasks = []
    for (let i = 1; i < this.state.count; i++) {
      tasks.push(JSON.parse(localStorage.getItem(i)));
    }
    return tasks;
  }

  setTask() {
    var task = {
      id: this.state.count,
      description: this.state.inputValue,
      status: "pending"
    };
    this.setState({
      count: this.state.count + 1 
    });
    localStorage.setItem(this.state.count, JSON.stringify(task));
  }

  handleChange(evt) {
    this.setState({
      inputValue: evt.target.value
    });
  }

  addTask() {
    this.setTask();
    this.setState({
      tasks: this.getTaskList()
    });
    document.getElementById("todoInput").value = "";
  }

  render() {
    const taskList = this.state.tasks.forEach(function(task) {
      return <Task value={task.description} />;
    });
    return (
      <div className="App">
        <div className="App-header">
          <h2>The 10001st Todo App</h2>
        </div>
        <p className="inputField">
          <input id="todoInput" type="text" onChange={this.handleChange} />
          <button onClick={this.addTask}>Add Task</button>
        </p>
        <form id="filterForm">
          <input type="radio" name="status" value="all" />
          <span>All</span>
          <input type="radio" name="status" value="complete" />
          <span>Completed</span>
          <input type="radio" name="status" value="pending" />
          <span>Pending</span>
        </form>
        <ul>
          {taskList}
        </ul>
      </div>
    );
  }
}

// HELPER FUNCTIONS
function search(nameKey, myArray) {
  for (var i = 0; i < myArray.length; i++) {
    if (myArray[i].name === nameKey) {
      return myArray[i];
    }
  }
}

export default App;
