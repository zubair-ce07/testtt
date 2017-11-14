import React from 'react';
import { Route, IndexRoute } from 'react-router';

import App from './components/app';
import Login from './components/login';
import Profile from './components/profile';
import SearchResults from './components/search_results';
import TrainerDetails from './components/trainer_details';
import TraineeDetails from './components/trainee_details';
import TrainerSignup from './components/trainer_signup';
import TraineeSignup from './components/trainee_signup';
import AssignmentDetails from './components/assignment_details';
import TechnologyDetails from './components/technology_details';


export default (
    <Route path="/" component={ App }>
        <IndexRoute component={ Login }/>
        <Route path="/trainer_signup" component={ TrainerSignup } />
        <Route path="/trainee_signup" component={ TraineeSignup } />
        <Route path="/profile" component={ Profile } />
        <Route path="/search/:q" component={ SearchResults } />
        <Route path="/trainers/:id" component={ TrainerDetails } />
        <Route path="/trainees/:id" component={ TraineeDetails } />
        <Route path="/assignments/:id" component={ AssignmentDetails } />
        <Route path="/technologies/:id" component={ TechnologyDetails } />
    </Route>
);