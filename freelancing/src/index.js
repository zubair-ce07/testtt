import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux'

import './index.css';
import configureStore from './store';
import App from './components/app/App';

ReactDOM.render(
  <Provider store={configureStore()}>
    <App />
  </Provider >,
  document.getElementById('root')
);
