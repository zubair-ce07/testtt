import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import MainPage from './MainPage';
import registerServiceWorker from './registerServiceWorker';


fetch('http://127.0.0.1:8000/get-all-mems/').then(response => {
     response.json().then(data => {
          ReactDOM.render(<MainPage mems={data}/>, document.getElementById('root'));
     });
});

registerServiceWorker();
