import React from 'react'
import {Route} from 'react-router-dom'

import InputTODO from './Input'
import CustomJumbotron from './HomePage'
import Footer from './Common/Footer'
import Navigation from './Common/Header'
import Todos from './Todos/Todos'

var toastr = require('toastr');

class App extends React.Component {
    constructor() {
        super()

        this.state = {
            taskList: [],
            task: {
                index: 0,
                subject: '',
                pending: true
            }
        }

        this.handleInput = this.handleInput.bind(this)
        this.onSubmit = this.onSubmit.bind(this)
        this.handleCheckClick = this.handleCheckClick.bind(this)
        this.handleDeleteTask = this.handleDeleteTask.bind(this)
        this.count = 0

        this.handlers = {
            handleCheckClick: this.handleCheckClick,
            handleDeleteTask: this.handleDeleteTask
        }
    }

    handleDeleteTask(e){
        let updateTaskList = []

        this.state.taskList.forEach(function(element) {
            if(e !== element.index){
                updateTaskList.push(element)
            }
            else{

            }
        });
        this.setState({taskList: updateTaskList})
    }

    handleCheckClick(e) {
        let updateTaskList = this.state.taskList.slice()

        updateTaskList.forEach(function(element) {
            if(parseInt(e.target.value, 10) === element.index){
                element.pending = !element.pending
            }
            return element
        });

        this.setState({taskList: updateTaskList})
    }

    onSubmit(e) {
        const newTaskList = this.state.taskList.slice()
        newTaskList.push(this.state.task)

        if (this.state.task.subject && !(this.state.task.subject.includes(' '))) {
            this.count++
            document.getElementById('inputBox').value = ''
            const task = {
                subject: ''
            }
            this.setState({
                taskList: newTaskList,
                task: task
            })
            toastr.success('Task Added')
        } else {
            toastr.error('Incorrect Input')
        }

    }

    handleInput(e) {
        const task = {
            index: this.count,
            subject: e.target.value,
            pending: true
        }

        this.setState({task: task})
        document.getElementById('inputBox')
    }

    render() {
        return (
            <div>
                <Route
                    path='/'
                    component={Navigation}
                />

                <div className="container">
                    <Route
                        exact
                        path="/"
                        component={CustomJumbotron}
                    />

                    <div className="group">
                        <Route
                            path="/home"
                            render = {
                                () => (
                                    <InputTODO
                                        onChange={this.handleInput}
                                        onAddClick={this.onSubmit}
                                    />
                                )
                            }
                        />
                        <Route
                            path="/home"
                            component = {
                                ()=> (
                                    <Todos
                                        taskList = {this.state.taskList}
                                        handlers = {this.handlers}
                                        completed = {false}
                                    />
                                )
                            }
                        />
                    </div>

                    <div className="group">

                        <Route
                            path="/todos"
                            component = {
                                ()=> (
                                    <Todos
                                        taskList = {this.state.taskList}
                                        handlers = {this.handlers}
                                        completed = {true}
                                    />
                                )
                            }
                        />
                    </div>

                </div>
                <Footer />
            </div>
        )
    }
}

export default App
