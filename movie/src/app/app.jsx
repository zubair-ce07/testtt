import React from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";
import { AuthContainer, HomeContainer } from "../containers";
import { PrivateRoute } from "../hocs/";

class App extends React.Component {
    
  render() {
    
    return (
      <Router>
          
          <PrivateRoute exact path="/" component={HomeContainer} isAuthenticated={true} />
          <Route path="/register" component={AuthContainer} />
        

         
       
      </Router>
    );
  }
}

export { App };
