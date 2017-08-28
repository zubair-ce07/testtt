import {createStore} from "redux";
import * as ReactDOM from "react-dom";
import * as React from "react";
import {Provider} from "react-redux";
import "./index.css";
import Header from "./components/Header";
import TodoList from "./components/TodoList";
import todoApp from "./reducers/todoApp";


const TodoApp = () => (
    <div>
        <Header/>
        <TodoList/>
    </div>
);

ReactDOM.render(
    <Provider store={createStore(todoApp)}>
        <TodoApp/>
    </Provider>
    ,
    document.getElementById('root')
);
