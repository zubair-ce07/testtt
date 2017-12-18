import React from 'react';
import ReactDOM from 'react-dom';
import { createStore, applyMiddleware } from 'redux'
import thunkMiddleware from 'redux-thunk'
import {Provider} from 'react-redux';
import weatherApp from './reducers'
import App from './components/App.js';
import registerServiceWorker from './registerServiceWorker';


const store = createStore(weatherApp, applyMiddleware(thunkMiddleware));
ReactDOM.render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById('root')
);
registerServiceWorker();
