import React from 'react'

import TodoItem from './TodoItem'

const TodoList = (props) => {

    var handlers = props.handlers
    var todoItems = props.taskList.map(function(element) {
        return <TodoItem key={element.index} task={element} handlers={handlers}/>
    });

    if(props.completed){
        var completed = props.taskList.reduce(function(arr, element){
            if(!element.pending){
                arr.push(<TodoItem key={element.index} task={element} handlers={handlers}/>)
            }
            return arr
        }, [])
    }

    return(
        <div>
            {(todoItems.length > 0 ? 'All':'')}
            {todoItems}
            {props.completed && completed.length > 0  ? 'Completed':''}
            {completed}
        </div>
    )
}

export default TodoList
