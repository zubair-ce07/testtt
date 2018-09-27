import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';

import { Provider } from 'react-redux';
import configureStore from './redux/store';

import App from './components/app';
import registerServiceWorker from './registerServiceWorker';

const rootEl = document.getElementById('root');
const store = configureStore();

const render = () => {
  ReactDOM.render(
    <Provider store={store}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </Provider>,
    rootEl
  );
};

// eslint-disable-next-line
if (module.hot) {
  // eslint-disable-next-line
  module.hot.accept('./components/app', render);
}


render();
registerServiceWorker();
