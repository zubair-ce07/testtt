import React, { Component } from 'react';
import './App.css';
import Player from './Player';
import List from './List';
import Search from './Search';
import { Route } from 'react-router-dom'

class App extends Component {


    render() {
        return (
            <div>
                <Route path='/' component={Search}/>
                <Route path='/search/:query' exact render={(props) => <List {...props} />}  />
                <Route path='/play/:id' component={Player}/>
            </div>
        );
    }
}
export default App;