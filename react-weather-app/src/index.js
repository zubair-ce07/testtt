import React from 'react';
import ReactDOM from 'react-dom';

import {Provider} from 'react-redux';
import {createStore, applyMiddleware} from 'redux';
import ReduxPromise from 'redux-promise';

import './index.css';
import App from './components/app';

import reducers from './reducers';

import * as serviceWorker from './serviceWorker';

const createStoreWithMiddleware = applyMiddleware(ReduxPromise)(createStore);

ReactDOM.render(
    <Provider store={createStoreWithMiddleware(reducers)}>
        <App />
    </Provider>
    , document.getElementById('root'));

serviceWorker.unregister();
