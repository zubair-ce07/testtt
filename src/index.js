



import React from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux';
import App from './components/App';
import configureStore from './store/configureStore';
import registerServiceWorker from './registerServiceWorker';
import {loadWeatherData} from './actions/weather';
const store = configureStore()

//store.dispatch(loadWeatherData());

render(
    <Provider store={store}>
<App/>
    </Provider>,
    document.getElementById('root')
);
registerServiceWorker();
