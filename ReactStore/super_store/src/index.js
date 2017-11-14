
import React from 'react'
import ReactDOM from 'react-dom'
import {BrowserRouter} from 'react-router-dom'

import MainApp from './components/Main'


ReactDOM.render(
    <BrowserRouter>
        <MainApp />
    </BrowserRouter>,
document.getElementById('root'))
