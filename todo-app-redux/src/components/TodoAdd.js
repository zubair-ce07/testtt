import * as React from "react";
import {connect} from "react-redux";
import {actions} from "../config";


let indexOfNextTodo = 0;

let TodoAdd = ({dispatch}) => {
    let inputText;

    const addTodoButtonHandler = () => {
        dispatch({
            type: actions.ADD_TODO,
            text: inputText.value,
            index: indexOfNextTodo++,
        });
        inputText.value = '';
    };

    return (
        <div className="todoAdder">
            <input ref={node => inputText = node}/>
            <button onClick={addTodoButtonHandler}>
                Add Todo
            </button>
        </div>
    );

};

TodoAdd = connect()(TodoAdd);

export default TodoAdd;
