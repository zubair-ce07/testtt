import React from 'react'
import {Route, withRouter, Switch} from 'react-router-dom'


import InputTODO from './Input'
import ListTODO from './List'
import CustomJumbotron from './HomePage'
import Footer from './Common/Footer'
import Navigation from './Common/Header'


class App extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            taskList: [],
            task: {
                index: 0,
                subject: '',
                pending: true
            }
        }
        const c = 0
        this.changeInput = this.handleInput.bind(this)
        this.onSubmit = this.onSubmit.bind(this)
        this.handleCheckClick = this.handleCheckClick.bind(this)
        this.handleDeleteTask = this.handleDeleteTask.bind(this)
        this.count = 0
    }

    handleDeleteTask(e){
        let updateTaskList = []

        this.state.taskList.forEach(function(element) {
            if(e != element.index){
                updateTaskList.push(element)
            }
        });

        this.setState({taskList: updateTaskList})
    }

    handleCheckClick(e) {
        let updateTaskList = this.state.taskList.slice()

        updateTaskList.forEach(function(element) {
            if(e.target.value == element.index){
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
            this.setState({taskList: newTaskList})
            this.count++
            document.getElementById('inputBox').value = ''
        } else {
            alert('Incorrect Input')
        }

    }
    handleInput(e) {
        const task = {
            index: this.count,
            subject: e.target.value,
            pending: true
        }

        this.setState({task: task})
    }

    render() {
        var Completed = this.state.taskList.map(function(item){
            if(!item.pending){
                return item
            }
        })
        return (
            <div>
                <Route
                    path='/'
                    component={Navigation}
                />

                <div className="container">
                    <Switch>
                        <Route
                            exact
                            path="/"
                            component={CustomJumbotron}

                        />


                        <Route
                            path="/home"
                            render = {
                                () => (
                                <div className="group">

                                    <InputTODO
                                        change={this.changeInput}
                                        onAddClick={this.onSubmit}
                                    />

                                    <br/><br/><br/>

                                    <ListTODO
                                        taskList={this.state.history}
                                        onCheckClick={this.handleCheckClick}
                                        onDeleteTask={this.handleDeleteTask}
                                    />

                                </div>
                                )}
                        />

                        <Route

                            path="/todos"
                            render = {
                                    ()=> (
                                        <div className="group">
                                        All:
                                            <ListTODO
                                                taskList={this.state.history}
                                                onCheckClick={this.handleCheckClick}
                                                onDeleteTask={this.handleDeleteTask}
                                            />

                                        Completed:
                                            <ListTODO
                                                taskList={Completed}
                                                onCheckClick={this.handleCheckClick}
                                                onDeleteTask={this.handleDeleteTask}
                                            />

                                        </div>)
                                }
                        />
                    </Switch>

                </div>
                <Footer />
            </div>
        )
    }
}

export default App
