import React from "react"
import NavBar from "./Navbar"
import "../App.css"

const App = props => {
  return (
    <div className="container">
      <NavBar />
      {props.children}
    </div>
  )
}

export default App
