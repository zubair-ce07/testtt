import React from 'react'
import InputTODO from './Input'
import ListTODO from './List'
import Navigation from './nav'
import {Route} from 'react-router-dom'

class App extends React.Component {
    constructor() {
        super()
        this.state = {
            history: [],
            task: {
                index: 0,
                subject: '',
                pending: true
            }
        }
        this.changeInput = this
            .handleInput
            .bind(this)
        this.onSubmit = this
            .onSubmit
            .bind(this)
        this.handleCheckClick = this
            .handleCheckClick
            .bind(this)
        this.handleDeleteTask = this.handleDeleteTask.bind(this)
        this.count = 0
    }

    handleDeleteTask(e){
        let update_history = []

        this.state.history.forEach(function(element) {
            if(e != element.index){
                update_history.push(element)
            }
        });
        this.setState({history: update_history})
    }

    handleCheckClick(e) {
        let update_history = this
            .state
            .history
            .slice()

        update_history.forEach(function(element) {
            if(e.target.value == element.index){
                element.pending = !element.pending
            }
            return element
        });
        this.setState({history: update_history})
    }

    onSubmit(e) {
        const newHistory = this
            .state
            .history
            .slice()
        newHistory.push(this.state.task)

        if (this.state.task.subject && !(this.state.task.subject.includes(' '))) {
            this.setState({history: newHistory})
            this.count++;
            document
                .getElementById('inputBox')
                .value = ''
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
        var Completed = this.state.history.map(function(item){
            if(!item.pending){
                return item
            }
        })
        return (
            <div>

                <Navigation/>
                <div className="container">

                    <h1 className="text-center">
                        Todo App!
                    </h1>

                    <Route path="/home" render = {
                        () => (
                        <div className="group">
                            <InputTODO change={this.changeInput} onAddClick={this.onSubmit}/>
                            <br/><br/><br/>
                            <ListTODO taskList={this.state.history} onCheckClick={this.handleCheckClick} onDeleteTask={this.handleDeleteTask}/>
                        </div>
                    )} />

                    <Route path="/all" render = {
                        ()=> (<div className="group">
                            All:
                                <ListTODO taskList={this.state.history} onCheckClick={this.handleCheckClick} onDeleteTask={this.handleDeleteTask}/>
                            Completed:
                                <ListTODO taskList={Completed} onCheckClick={this.handleCheckClick} onDeleteTask={this.handleDeleteTask}/>
                            </div>)
                    } />

                </div>
            </div>
        )
    }
}

export default App
