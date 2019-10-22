import React, { Component } from 'react';
import  { BrowserRouter, Route } from 'react-router-dom';

import Navbar from './components/layout/navbar';
import Home from './components/home';
import Register from './components/auth/register';
import Login from './components/auth/login';
import Footer from './components/layout/footer'
import Product from './components/products/product';
import logout from './components/auth/logout';

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
            <Route path='/logout' component={logout} />
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
