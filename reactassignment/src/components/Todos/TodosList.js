import React from 'react'

import TodoItem from './TodoItem'

class TodoList extends React.Component{

    render(){
        var handlers = this.props.handlers
        var todoItems = this.props.taskList.map(function(element) {
            return <TodoItem key={element.index} task={element} handlers={handlers}/>
        });

        if(this.props.completed){
            var completed = this.props.taskList.reduce(function(arr, element){
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
                {this.props.completed && completed.length > 0  ? 'Completed':''}
                {completed}
            </div>
        )
    }
}


export default TodoList
