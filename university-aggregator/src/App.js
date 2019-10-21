import React from "react";
import { BrowserRouter as Router, Switch, Route , Redirect } from "react-router-dom";

import { Program } from "./components/Program";
import { Course } from "./components/Course";
import { Home } from "./components/Home";
import { Header } from "./components/Header";

import "./App.css";
import { Login } from "./components/Login/Login";

const App = () => (
  <div className="App">
    <Header />
    <Router>
      <div>
        <Switch>
          <Route name="login" path="/login" component={Login}></Route>
          <Route
            name="programs"
            path="/institutions/:id/programs"
            component={Program}
          ></Route>
          <Route
            name="courses"
            path="/programs/:id/courses/"
            component={Course}
          ></Route>
          <Route name="home" path="/home" component={Home}></Route>
          <Redirect exact from='/' to='/login'/>
        </Switch>
      </div>
    </Router>
  </div>
);

export default App;
