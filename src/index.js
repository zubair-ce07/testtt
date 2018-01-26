/*created by Zulqarnain on 24-01-2018*/
import {createStore, applyMiddleware, combineReducers} from "redux";
import logger from "redux-logger";
import React from "react";
import ReactDOM from "react-dom";
import Root from "./app.jsx";
import {Provider} from 'react-redux'


const changeReducer = (state = {
    showSignUp: false,
    showLogin: true
}, action) => {
    switch (action.type) {
        case 'SHOW_LOGIN':
            state = {
                showLogin: true,
                showSignUp: false
            };
            break;
        case 'SHOW_SIGN_UP':
             state = {
                showLogin: false,
                showSignUp: true
            };
            break;
        default:
            break;
    }
    return state;
};

const store = createStore(combineReducers({reducer : changeReducer}),
    {},
    applyMiddleware(logger)
);

ReactDOM.render(
    <Provider store={store}>
        <Root />
    </Provider>,
    document.getElementById('root'));