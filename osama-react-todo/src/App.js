import React, { Component } from "react";
import logo from "./logo.svg";
import "./App.css";

class Task extends Component {
  constructor(props) {
    super();
    this.handleClick = this.handleClick.bind(this);
    this.state = {
      id: props.id,
      description: props.value
    };
  }

  handleClick(evt) {
    // window.confirm('Complete this task? \n"' + evt.target.innerHTML + '"')
    if (
      window.confirm('Complete this task? \n"' + evt.target.innerHTML + '"')
    ) {
      var temp = JSON.parse(localStorage.getItem(this.state.id));
      temp.status = "complete";
      localStorage.setItem(this.state.id, JSON.stringify(temp));
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
    this.getTask = this.getTask.bind(this);
    this.getTaskList = this.getTaskList.bind(this);
    this.setTaskList = this.setTask.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.addTask = this.addTask.bind(this);
    this.count = Boolean(localStorage.getItem("count"))
      ? localStorage.getItem("count")
      : 0;
    this.state = {
      count: this.count,
      tasks: this.getTaskList(),
      inputValue: ""
    };
  }

  // gets a task object from localStorage
  getTask(index) {
    return JSON.parse(localStorage.getItem(+index));
  }

  getTaskList() {
    var tasks = [];
    for (let i = 0; i < this.count; i++) {
      var temp = this.getTask(i);
      tasks[i] = temp;
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
    this.count += 1;
    localStorage.setItem(this.state.count, JSON.stringify(task));
    localStorage.setItem("count", ++this.state.count);
  }

  handleInputChange(evt) {
    this.setState({
      inputValue: evt.target.value
    });
  }

  handleRadioChange(evt) {
    var filterStatus = evt.target.value;
    var tasks = this.getTaskList();
    if (filterStatus !== "all") {
      tasks = tasks.filter(element => {
        return element.status === filterStatus;
      });
    };    
    
    this.setState({
      tasks: tasks
    });
  }

  addTask() {
    console.log(this);
    this.setTask();
    this.setState({
      tasks: this.getTaskList()
    });
    document.getElementById("todoInput").value = "";
  }

  render() {
    const taskList = this.state.tasks.map(task => {
      if (task) {
        return <Task id={task.id} value={task.description} />;
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

// HELPER FUNCTIONS
function search(nameid, myArray) {
  for (var i = 0; i < myArray.length; i++) {
    if (myArray[i].name === nameid) {
      return myArray[i];
    }
  }
}

export default App;
