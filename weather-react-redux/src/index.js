import React from 'react';
import ReactDOM from 'react-dom';
import thunk from 'redux-thunk';
import { createStore, applyMiddleware } from 'redux';
import { Provider } from 'react-redux';
import './index.css';
import App from './components/App';
import allReducers from './reducers';
import registerServiceWorker from './registerServiceWorker';

const middleware = applyMiddleware(thunk);
const store = createStore(allReducers, middleware);

ReactDOM.render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById('root'));
registerServiceWorker();
