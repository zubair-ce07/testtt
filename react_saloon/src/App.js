import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom'

import Signup from './components/signup'
import Login from './components/login'
import Navbar from './components/navbar'

function App() {
  return (
    <BrowserRouter >
      <div className="App">
        <Switch>
          <Route exact path='/login' component={Login} />
          <Route exact path='/signup' component={Signup} />
          <Route path='/' component={Navbar} />
        </Switch>
      </div>
    </BrowserRouter>
  );
}

export default App;
