import React from 'react';
import ReactDOM from 'react-dom';
import {Provider} from 'react-redux'
import { createStore, applyMiddleware } from 'redux'
import thunk from 'redux-thunk';
import rootReducer from './reducers/index';
import SocialNetwork from './components/MainApp/SocialNetwork'
import {loadState} from './localStorage'
import './index.css';
 
const persisted_state = {authReducer: loadState()}
let store = createStore(
	rootReducer,
	persisted_state,
	applyMiddleware(thunk)
);



ReactDOM.render(
	<Provider store={ store }>
  		<SocialNetwork />
  	</Provider>,
  document.getElementById('root')
);	