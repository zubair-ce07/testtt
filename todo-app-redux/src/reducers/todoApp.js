import {combineReducers} from "redux";
import * as React from "react";
import {actions, filters} from "../config";


const todo = (state, action) => {
    switch (action.type) {
        case actions.ADD_TODO:
            return {
                index: action.index,
                text: action.text,
                completed: false
            };
        case actions.TOGGLE_TODO:
            return state.index === action.index ? {
                ...state,
                completed: !state.completed
            } : state;
        default:
            return state;
    }
};

const todos = (state = [], action) => {
    switch (action.type) {
        case actions.ADD_TODO:
            return [
                ...state,
                todo(undefined, action),
            ];
        case actions.TOGGLE_TODO:
            return state.map((t) => {
                return todo(t, action);
            });
        default:
            return state;
    }
};


const visibilityFilter = (state = filters.SHOW_ALL, action) => {
    switch (action.type) {
        case actions.SET_VISIBILITY_FILTER:
            return action.filter;
        default:
            return state;
    }
};


const todoApp = combineReducers({
    todos,
    visibilityFilter
});

export default todoApp;
