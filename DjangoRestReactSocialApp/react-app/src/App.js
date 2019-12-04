import React, { Component } from 'react'
import AppRoutes from 'routes/app.routes'
import './App.css'

class App extends Component {
  render () {
    return (
      <div className="App">
        <AppRoutes></AppRoutes>
      </div>
    )
  }
}

export default App
