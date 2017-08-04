import React from 'react'
import {Route} from 'react-router-dom'

import App from './App'
import Login from './LogInOut/Login'

const MainApp = (props) => {
    return (
        <div>
            <Route
                path="/app/login/"
                component={Login}
            />
            <Route
                exact
                path="/"
                component={App}
            />
        </div>
    )
}

export default MainApp
