import React from 'react'
import {Router, Route} from 'react-router';
import LoginSignup from '../containers/LoginSignup';
import Home from './home'
import { browserHistory} from 'react-router';
import UserMems from '../containers/UserMems';
import PublicMems from '../containers/PublicMems';
import Activities from '../containers/Activities';
import UserProfile from '../containers/UserProfile';
import AddCategory from '../containers/AddCategory';
import AddMem from '../containers/AddMem';
import EditProfile from '../containers/EditProfile';
import EditMem from '../containers/EditMem';

/*import '../assets/css/bootstrap.css';
import '../assets/css/font-awesome.css';
import '../assets/js/morris/morris-0.4.3.min.css';
import '../assets/css/custom-styles.css';
import '../assets/materialize/css/materialize.min.css'

import $ from 'jquery';
*/



const App = function () {
    return(
        <Router history={browserHistory}>
          <div>
                <Route exact path="/" component={LoginSignup}/>
                <Route path="/" component={Home}>
                    <Route path="/home" component={UserMems}/>
                    <Route path="/public" component={PublicMems}/>
                    <Route path="/activities" component={Activities}/>
                    <Route path="/profile:id" component={UserProfile}/>
                    <Route path="/addcategory" component={AddCategory}/>
                    <Route path="/addmem" component={AddMem}/>
                    <Route path="/editprofile:id" component={EditProfile}/>
                    <Route path="/editmem:id" component={EditMem}/>
                </Route>
          </div>
    </Router>

    );
}
export default App;