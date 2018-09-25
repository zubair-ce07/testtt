import React from 'react';
import SignIn from './SignIn'
import SignUp from './SignUp'
// import Dashboard from '../components/Dashboard'
import Profile from './Profile'
import ConsumerHome from './ConsumerHome'
import Home from './Home'
import UnPairedConsumers from './UnPairedConsumers'
import PairedConsumers from './PairedConsumers'
// import Master from './Master'
import { BrowserRouter as Router, Route } from "react-router-dom";
import Constants from '../utils/Constants'


const MyRouter = () => (
  <Router>
    <div>
      <Route exact path='/' component={HomePage}/>
      <Route exact path='/signin' component={SignInPage}/>
      <Route path='/signup' component={SignUpPage}/>
      <Route path='/unpaired-consumers' component={UnpairedConsumersPage}/>
      <Route path='/paired-consumers' component={PairedConsumersPage}/>
      <Route path='/my-donor' component={MyDonorPage}/>
      <Route path='/my-profile' component={MyProfilePage} />
    </div>
  </Router>
);

// const ReactMaster = () => {
//   <div>
//     <Master />
//   </div>
// }

const HomePage = () => (
  <div>
    <Home />
  </div>
);

const SignInPage = () => (
  <div>
    <SignIn />
  </div>
);

const SignUpPage = () => (
  <div>
    <SignUp />
  </div>
);

const UnpairedConsumersPage = () => (
  <div>
    {/* <Dashboard title="Avalaible Consumers"
      getUrl={Constants.unpairedConsumersGET}
      shouldPairButtonShow={true}
     /> */}
     <UnPairedConsumers />
  </div>
);

const PairedConsumersPage = () => (
  <div>
    {/* <Dashboard title="My Consumers"
      getUrl={Constants.pairedConsumerGET}
      shouldPairButtonShow={false}
    /> */}
    <PairedConsumers />
  </div>
);

const MyDonorPage = () => (
  <div>
    <ConsumerHome title="My Donor"
      getUrl={Constants.myDonorGET}
    />
  </div>
);

const MyProfilePage = () => (
  <div>
    <Profile title="My Profile"
      getUrl={Constants.myProfileGET}
      userId={localStorage.getItem('userId')}
    />
  </div>
);

export default MyRouter;
