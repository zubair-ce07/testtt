import React from 'react';
import SignIn from './SignIn'
import SignUp from './SignUp'
import Dashboard from './Dashboard'
import Profile from './Profile'
import ConsumerHome from './ConsumerHome'
import { BrowserRouter as Router, Route } from "react-router-dom";
import Constants from '../utils/Constants'

const MyRouter = () => (
  <Router>
    <div>
      <Route exact path='/' component={Home}/>
      <Route path='/signup' component={Signup}/>
      <Route path='/unpaired-consumers' component={UnpairedConsumers}/>
      <Route path='/paired-consumers' component={PairedConsumers}/>
      <Route path='/my-donor' component={MyDonor}/>
      <Route path='/my-profile' component={MyProfile} />
    </div>
  </Router>
);

const Home = () => (
  <div>
    <SignIn />
  </div>
);

const Signup = () => (
  <div>
    <SignUp />
  </div>
);

const UnpairedConsumers = () => (
  <div>
    <Dashboard title="Avalaible Consumers"
      getUrl={Constants.unpairedConsumersGET}
     />
  </div>
);

const PairedConsumers = () => (
  <div>
    <Dashboard title="My Consumers" getUrl={Constants.pairedConsumerGET}/>
  </div>
);

const MyDonor = () => (
  <div>
    <ConsumerHome title="My Donor" getUrl={Constants.myDonorGET}/>
  </div>
);

const MyProfile = () => (
  <div>
    <Profile title="My Profile" getUrl={Constants.myProfileGET} userId={localStorage.getItem('userId')}/>
  </div>
);

export default MyRouter;
