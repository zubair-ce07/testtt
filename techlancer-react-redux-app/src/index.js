import { Provider } from 'react-redux';
import React from 'react';
import ReactDOM from 'react-dom';

import App from './App';
import configureStore from './configureStore';
import 'bootstrap/dist/js/bootstrap.min.js';
import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';

const store = configureStore();

ReactDOM.render(
   <Provider store={store}>
      <App />
  </Provider>,
  document.getElementById('root')
);

