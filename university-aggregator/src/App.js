import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import { Program } from "./components/Program";
import { Course } from "./components/Course";
import { Home } from "./components/Home";
import { Header } from './components/Header';


import "./App.css";

const App = () => (
  <div className="App">
   < Header />
    <Router>
      <div>
        <Switch>
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
          <Route name="home" path="/" component={Home}></Route>
        </Switch>
      </div>
    </Router>
  </div>
);

export default App;
