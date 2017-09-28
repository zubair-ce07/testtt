import React from 'react';
import ReactDOM from 'react-dom';
import {Provider} from 'react-redux'
import { createStore } from 'redux'
import './index.css';
import rootReducer from './reducers/index';
import SocialNetwork from './components/MainApp/SocialNetwork'
import {loadState} from './localStorage'
 
const persisted_state = {authReducer: loadState()}
let store = createStore(
	rootReducer,
	persisted_state
);



ReactDOM.render(
	<Provider store={ store }>
		
  		<SocialNetwork />
  	</Provider>,
  document.getElementById('root')
);	