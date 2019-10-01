import React from "react";
import { connect } from "react-redux";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { AuthContainer } from "./auth";
import { HomeContainer } from "./home";
import { PrivateRoute } from "../hocs/";

class App extends React.Component {
  render() {
    return (
      <Router>
        <Switch>
          <PrivateRoute
            exact
            path="/"
            component={HomeContainer}
            isAuthenticated={this.props.isAuthenticated}
          />
          <Route path="/register" component={AuthContainer} />
        </Switch>
      </Router>
    );
  }
}

const mapStateToProps = state => ({
  isAuthenticated: state.authReducer.isAuthenticated
});
const AppContainer = connect(mapStateToProps)(App);

export { AppContainer };
