import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
import './App.css';
import { Program } from './components/programs.component';
import { Course } from './components/courses.component';
import { Home } from './components/home.component';

function App() {
  return (
    <div className="App">
       <Router>
      <div>
        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Switch>
          <Route name="programs" path="/institutions/:id/programs" component={Program}>
          </Route>
          <Route name="courses" path="/programs/:id/courses/" component={Course}>
          </Route>
          <Route name="home" path="/" component={Home} >
          </Route>
        </Switch>
      </div>
    </Router>
    </div>
  );
}

export default App;
