import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
import 'bootstrap/dist/css/bootstrap.css';
import {createStore, applyMiddleware} from 'redux';
import thunk from 'redux-thunk';
import rootReducer from './home/reducers/index';
import reducers from './home/reducers';
import { Provider } from 'react-redux'


const createStoreWithMiddleware = applyMiddleware(thunk)(createStore);
const store = createStore(rootReducer);

ReactDOM.render(
  <Provider store={createStoreWithMiddleware(reducers)}>
    <App />
  </Provider>,
   document.getElementById('root'));
registerServiceWorker();
