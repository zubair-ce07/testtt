import React from 'react';
import ReactDOM from 'react-dom';
import { createStore, applyMiddleware } from 'redux'
import thunkMiddleware from 'redux-thunk'
import {Provider} from 'react-redux';
import youtubeApp from './reducers'
import App from './App';
import registerServiceWorker from './registerServiceWorker';


const store = createStore(youtubeApp, applyMiddleware(thunkMiddleware));
ReactDOM.render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById('root')
);
registerServiceWorker();
