import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux'
import { ThemeProvider } from 'styled-components'

import './index.css';
import configureStore from './store';
import App from './components/app/App';
import theme from './components/app/theme';

ReactDOM.render(
  <Provider store={configureStore()}>
    <ThemeProvider theme={theme}>
      <App />
    </ThemeProvider>
  </Provider >,
  document.getElementById('root')
);
