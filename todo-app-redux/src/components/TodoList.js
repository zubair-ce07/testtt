import * as React from "react";
import PropTypes from "prop-types";
import {Nav, NavItem} from "react-bootstrap";
import {actions, filters} from "../config";


class TodoList extends React.Component {

    componentDidMount() {
        this.unsubscribed = this.context.store.subscribe(() =>
            this.forceUpdate()
        )
    }

    componentWillUnmount() {
        this.unsubscribed();
    }

    getVisibleTodos = (todos, visibilityFilter) => {
        switch (visibilityFilter) {
            case filters.SHOW_ALL:
                return todos;
            case filters.SHOW_COMPLETED:
                return todos.filter(
                    (todo) => todo.completed
                );
            case filters.SHOW_UNCOMPLETED:
                return todos.filter(
                    (todo) => !todo.completed
                );
            default:
                return todos;
        }
    };

    todoOnClickHandler = (selectedKey) => {
        this.context.store.dispatch({
                type: actions.TOGGLE_TODO,
                index: selectedKey,
            }
        );
    };


    render() {
        const {todos, visibilityFilter} = this.context.store.getState();
        const visibleTodos = this.getVisibleTodos(todos, visibilityFilter);
        return (
            <div className="todoList">
                <br/>
                <hr/>
                <Nav bsStyle="pills" stacked onSelect={this.todoOnClickHandler}>
                    {visibleTodos.map(todo => (
                        <NavItem
                            key={todo.index}
                            eventKey={todo.index}
                            active={!todo.completed}
                        >
                            {todo.completed ? <del>{todo.text}</del> : todo.text}
                        </NavItem>

                    ))}
                </Nav>
            </div>
        );
    }
}
TodoList.contextTypes = {
    store: PropTypes.object,
};

export default TodoList;
