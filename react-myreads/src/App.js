import './App.css'

import React from 'react'
import BookSearch from './components/BookSearch'
import DashBoard from './components/DashBoard'
import {HashRouter as Router, Route} from 'react-router-dom';


class App extends React.Component {
    render() {
        return (
            <Router>
                <div>
                    <Route exact path='/' component={DashBoard}/>
                    <Route exact path='/search' component={BookSearch}/>
                </div>
            </Router>
        );
    }
}

export default App
