import React from 'react'
import {ListGroup} from 'react-bootstrap/lib'

import TodoList from './TodosList'

const Todos = (props) => {
    return(
            <div>
                <ListGroup>
                    <TodoList
                        taskList={props.taskList}
                        handlers={props.handlers}
                        completed={props.completed}
                    />
                </ListGroup>
            </div>
        )
}

export default Todos
