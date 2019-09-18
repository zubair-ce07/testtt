import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import { createStore, applyMiddleware, combineReducers } from 'redux';
import { Provider } from 'react-redux';
import thunk from 'redux-thunk';
import ls from 'local-storage'

import saloonReducer from './reducers/saloonReducer'
import userReducer from './reducers/userReducer'

const reducer = combineReducers({
    user: userReducer,
    saloon: saloonReducer
})

const rootReducer = (state, action) => {
    if (action.type === 'LOGOUT_SUCESSFUL') {
        state = undefined
        ls.clear()
    }

    return reducer(state, action)
}

const store = createStore(rootReducer, applyMiddleware(thunk))

ReactDOM.render(<Provider store={store}><App /></Provider>, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
