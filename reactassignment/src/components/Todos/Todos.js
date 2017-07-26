import React from 'react'

import {ListGroup} from 'react-bootstrap/lib'

import TodoList from './TodosList'

class Todos extends React.Component{

    render(){
        return(
            <div>
                <ListGroup>
                    <TodoList taskList={this.props.taskList} handlers={this.props.handlers} completed={this.props.completed}/>
                </ListGroup>
            </div>
        )
    }

}

export default Todos
