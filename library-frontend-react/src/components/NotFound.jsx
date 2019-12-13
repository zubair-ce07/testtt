import { Link } from "react-router-dom"
import React from "react"
import confused from "static/images/confused.gif"
import urls from "urls"

const NOtFound = () => {
  return (
    <div id="page-not-found" className="container-fluid">
      <div className="header">
        <h1>Lost in Wild</h1>
      </div>
      <div className="error-main">
        <div className="error-info">
          <h2>
            4<img src={confused} alt="confused" />4
          </h2>
          <h3>SORRY</h3>
          <p>We could not find this page</p>
          <Link to={urls.home}> Home </Link>
        </div>
      </div>
    </div>
  )
}

export default NOtFound
