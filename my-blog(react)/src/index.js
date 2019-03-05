import React from 'react';
import ReactDOM from 'react-dom';
import { Router } from 'react-router-dom';

import { Provider } from 'react-redux';
import configureStore from './redux/store';
import history from './history';

import App from './components/app';
import registerServiceWorker from './registerServiceWorker';


const rootEl = document.getElementById('root');
const store = configureStore();

const render = () => {
  ReactDOM.render(
    <Provider store={store}>
      <Router history={history}>
        <App />
      </Router>
    </Provider>,
    rootEl
  );
};

if (module.hot) {
  module.hot.accept('./components/app', render);
}


render();
registerServiceWorker();
