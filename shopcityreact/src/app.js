import React, { Component } from 'react';
import  { BrowserRouter, Route } from 'react-router-dom';

import Navbar from './components/Navbar';
import Home from './components/Home';
import Register from './components/Register';
import Login from './components/login';
import Footer from './components/footer'
import Product from './components/Product';

class App extends Component
{
  render() 
  {
    return (
      <div>
        <BrowserRouter>
          <div className="App">
            <Navbar />
            <Route exact path='/' component={Home} />
            <Route path='/home' component={Home} />
            <Route path='/login' component={Login} />
            <Route path='/register' component={Register} />
            <Route path='/product/:product_id' component={Product} />
            <br/>
            <br/>
            <br/>
            <Footer />
          </div>
        </BrowserRouter>
      </div>
    );
  }
}

export default App;
